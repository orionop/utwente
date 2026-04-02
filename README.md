# Setup & Run

## 1. Install MCAP storage plugin (system-level, one time, needs sudo)
```bash
sudo apt install ros-humble-rosbag2-storage-mcap -y
```

## 2. Clone repo
```bash
git clone https://github.com/orionop/utwente.git
cd utwente
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

## 6. Copy bag data manually (gitignored)
```bash
cp -r /path/to/source/lfdws_trial_002 ~/Desktop/utwente/lfdws_trial_002
```

## 7. Run pipeline
```bash
python3 unbag_pipeline.py --path ~/Desktop/utwente/lfdws_trial_002
```

## 8. Output
- Per-topic CSVs written to the bag folder
- Combined merged CSV written to the bag folder
- Images (if any image topics) saved as PNGs

## Notes
- Every new terminal session: re-run steps 3 and 4 before running the script
- Bag data files (`.mcap`, `.pickle`, `.csv`) are gitignored — copy them manually to the bag folder
- Deactivate venv: `deactivate`
