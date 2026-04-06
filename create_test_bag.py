"""
Create a small test MCAP bag with image topics.
Used to validate that unbag_pipeline.py correctly:
  1. Extracts images as PNGs
  2. Puts PNG filenames (not binary) in the CSV

Run on Lab PC (needs ROS 2 Jazzy):
    source /opt/ros/jazzy/setup.bash
    python3 create_test_bag.py
"""

import os
import io
import numpy as np
from PIL import Image as PILImage

from rosbag2_py import SequentialWriter, StorageOptions, ConverterOptions
from rosbag2_py._storage import TopicMetadata
from rclpy.serialization import serialize_message
from rclpy.clock import Clock
from sensor_msgs.msg import Image, CompressedImage
from std_msgs.msg import Header
from builtin_interfaces.msg import Time


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "test_image_bag")
BAG_NAME = "test_image_bag"
NUM_FRAMES = 5


def make_color_image(width, height, frame_idx):
    """Generate a distinct colored image per frame (gradient + text-like pattern)."""
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Different dominant color per frame
    colors = [
        (255, 60, 60),    # red
        (60, 255, 60),    # green
        (60, 60, 255),    # blue
        (255, 255, 60),   # yellow
        (255, 60, 255),   # magenta
    ]
    r, g, b = colors[frame_idx % len(colors)]

    # Gradient fill
    for y in range(height):
        frac = y / height
        img[y, :, 0] = int(r * (1 - frac * 0.5))
        img[y, :, 1] = int(g * (1 - frac * 0.5))
        img[y, :, 2] = int(b * (1 - frac * 0.5))

    # Add a white rectangle with frame number (visual marker)
    cx, cy = width // 2, height // 2
    size = 20 + frame_idx * 5
    img[cy - size:cy + size, cx - size:cx + size] = 255

    return img


def create_raw_image_msg(img_array, timestamp_ns, frame_id="camera_raw"):
    """Create a sensor_msgs/msg/Image from numpy array."""
    msg = Image()
    msg.header = Header()
    msg.header.stamp = Time(
        sec=int(timestamp_ns // 1_000_000_000),
        nanosec=int(timestamp_ns % 1_000_000_000),
    )
    msg.header.frame_id = frame_id
    msg.height, msg.width = img_array.shape[:2]
    msg.encoding = "rgb8"
    msg.is_bigendian = False
    msg.step = msg.width * 3
    msg.data = img_array.tobytes()
    return msg


def create_compressed_image_msg(img_array, timestamp_ns, frame_id="camera_compressed"):
    """Create a sensor_msgs/msg/CompressedImage (JPEG) from numpy array."""
    pil_img = PILImage.fromarray(img_array, "RGB")
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG", quality=90)

    msg = CompressedImage()
    msg.header = Header()
    msg.header.stamp = Time(
        sec=int(timestamp_ns // 1_000_000_000),
        nanosec=int(timestamp_ns % 1_000_000_000),
    )
    msg.header.frame_id = frame_id
    msg.format = "jpeg"
    msg.data = buf.getvalue()
    return msg


def main():
    bag_path = os.path.join(OUTPUT_DIR, BAG_NAME)
    os.makedirs(bag_path, exist_ok=True)

    # Writer setup
    storage_options = StorageOptions(uri=bag_path, storage_id="mcap")
    converter_options = ConverterOptions("", "")
    writer = SequentialWriter()
    writer.open(storage_options, converter_options)

    # Register topics
    raw_topic = TopicMetadata(
        name="/camera/image_raw",
        type="sensor_msgs/msg/Image",
        serialization_format="cdr",
    )
    compressed_topic = TopicMetadata(
        name="/camera/image_compressed",
        type="sensor_msgs/msg/CompressedImage",
        serialization_format="cdr",
    )
    writer.create_topic(raw_topic)
    writer.create_topic(compressed_topic)

    # Write frames
    base_time_ns = 1700000000_000_000_000  # arbitrary start time
    dt_ns = 100_000_000  # 100ms between frames (10 Hz)

    for i in range(NUM_FRAMES):
        t = base_time_ns + i * dt_ns
        img = make_color_image(320, 240, i)

        # Raw image
        raw_msg = create_raw_image_msg(img, t)
        writer.write("/camera/image_raw", serialize_message(raw_msg), t)

        # Compressed image
        comp_msg = create_compressed_image_msg(img, t)
        writer.write("/camera/image_compressed", serialize_message(comp_msg), t)

        print(f"  Frame {i + 1}/{NUM_FRAMES} written")

    del writer
    print(f"\nTest bag created at: {bag_path}/")
    print(f"  {NUM_FRAMES} raw + {NUM_FRAMES} compressed = {NUM_FRAMES * 2} total messages")
    print(f"\nNow run:")
    print(f"  python3 unbag_pipeline.py --path {bag_path}")


if __name__ == "__main__":
    main()
