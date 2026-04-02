# Setup & Run

## 1. Install MCAP storage plugin (system-level, one time, needs sudo)
```bash
sudo apt install ros-humble-rosbag2-storage-mcap -y
```

## 2. Clone repo
```bash
git clone https://github.com/orionop/utwente.git
cd Desktop/anurag_ws/utwente-main
```

## 3. Source ROS2
```bash
source /opt/ros/humble/setup.bash
```

## 4. Create venv (inherits ROS2 system packages)
```bash
python3 -m venv --system-site-packages venv
source venv/bin/activate
```

## 5. Install pip dependencies
```bash
pip install pillow numpy
```

## 6. Run pipeline
```bash
python3 unbag_pipeline.py --path ~/Desktop/Desktop/anurag_ws/utwente-main/lfdws_trial_002/lfdws_trial_002
```

## 7. Output
- Per-topic CSVs written to the bag folder
- Combined merged CSV written to the bag folder
- Images (if any image topics) saved as PNGs

## Notes
- Every new terminal session: re-run steps 3 and 4 before running the script
- Deactivate venv: `deactivate`
