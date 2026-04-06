# ROS 2 Bag → CSV Pipeline (RLBD)

> **University of Twente / NAKAMA Robotics Lab**
> Remote collaboration: Robot Learning from Demonstration

## Overview

Extracts ROS 2 bag files (MCAP format) into per-topic CSVs + combined merged CSV.
Images (if any) are saved as PNGs with filename references in the CSV.

### Repo Structure

```
.
├── bag_to_csv.py              # Mark's original exporter (reference)
├── unbag_pipeline.py          # Main pipeline script (use this)
├── lfdws_trial_002/           # Trial data from the lab
│   ├── lfdws_trial_002/       # Bag folder
│   │   ├── lfdws_trial_002_0.mcap   # [INPUT]  Raw bag data
│   │   ├── metadata.yaml             # [INPUT]  Bag metadata
│   │   ├── *.csv                      # [OUTPUT] Per-topic + merged CSVs
│   │   └── *.pickle                   # [OUTPUT] Pickled data
│   └── src/                   # Lab ROS2 node configs (bota_driver, etc.)
└── README.md
```

---

## Setup on Lab PC (Ubuntu 24.04 + ROS 2 Jazzy)

### First-time setup

```bash
# 1. Install MCAP storage plugin (usually bundled with Jazzy, but just in case)
sudo apt install ros-jazzy-rosbag2-storage-mcap -y

# 2. Clone repo
cd ~/Desktop/anurag_ws
git clone https://github.com/orionop/utwente.git rlbd
cd rlbd

# 3. Source ROS 2 Jazzy
source /opt/ros/jazzy/setup.bash

# 4. Create venv (inherits ROS2 system packages)
python3 -m venv --system-site-packages venv
source venv/bin/activate

# 5. Install pip dependencies
pip install pillow numpy
```

### Run pipeline

```bash
# Every new terminal session, run these first:
cd ~/Desktop/anurag_ws/rlbd
source /opt/ros/jazzy/setup.bash
source venv/bin/activate

# Run the pipeline
python3 unbag_pipeline.py --path ./lfdws_trial_002/lfdws_trial_002
```

### Push results back to GitHub (from lab PC)

```bash
cd ~/Desktop/anurag_ws/rlbd
git add -A
git commit -m "pipeline output from lab PC"
git push origin main
```

---

## Pull latest on either device

```bash
# Mac (from repo root)
cd "/Users/anuragx/Desktop/Fall 2027/utwente"
git pull origin main

# Lab PC
cd ~/Desktop/anurag_ws/rlbd
git pull origin main
```

---

## Quick test command (Lab PC — full copy-paste block)

```bash
cd ~/Desktop/anurag_ws/rlbd && \
git pull origin main && \
source /opt/ros/jazzy/setup.bash && \
source venv/bin/activate && \
python3 unbag_pipeline.py --path ./lfdws_trial_002/lfdws_trial_002
```

---

## Output

- Per-topic CSVs written to the bag folder
- Combined merged CSV written to the bag folder
- Images (if any image topics) saved as PNGs
- `topics_map.json` mapping CSV files to original topic names

## Notes

- Every new terminal session: re-source ROS 2 and activate venv before running
- Deactivate venv: `deactivate`
- Tested on: **ROS 2 Jazzy Jalisco** (Ubuntu 24.04)
- Input bag: 2 topics — `/bota_post/wrench_body_compensated` (WrenchStamped) + `/NS_1/franka_robot_state_broadcaster/current_pose` (PoseStamped)
- No custom message types needed — uses standard `geometry_msgs`
