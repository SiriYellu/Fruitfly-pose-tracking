# Task 3: Fly Tracking

## Overview
This task implements integrated pose estimation and multi-object tracking algorithms to associate detected flies across frames, generating continuous behavioral trajectories. The system uses the best YOLO11m-pose model from Task 2 (97% mAP50) for pose estimation, then applies advanced tracking algorithms to handle fly re-entry, partial occlusion, and ID reassignment throughout video sequences.



### Core Implementation Files:
- `scripts/fly_tracker.py` - Main tracking system implementation
- `scripts/run_integrated_tracking.py` - Integrated tracking with Task 2 results
- `scripts/run_behavioral_analysis.py` - Behavioral analysis for tracking results

### Supporting Files:
- `configs/tracking_config.yaml` - Configuration parameters
- `results/` - Analysis outputs and results

## Methodology

### 1. Integrated Pipeline
- **Pose Estimation**: YOLO11m-pose model (97% mAP50 from Task 2)
- **Model Selection**: Automatic detection of best trained model
- **Input Processing**: Direct image processing (JPG/PNG) or pre-labeled data
- **Output**: Continuous trajectories with pose information

### 2. Tracking Algorithm
- **Primary Method**: Pose-based Multi-Object Tracking (MOT)
- **Association Strategy**: Hungarian algorithm with pose similarity
- **Distance Metric**: Weighted combination of pose and bounding box distances
- **ID Management**: Automatic reassignment for re-entering flies

### 3. Key Features
- **Pose-based Association**: Uses keypoint similarity for robust tracking
- **Occlusion Handling**: Maintains tracks during temporary disappearances
- **Re-entry Detection**: Reassigns IDs when flies reappear
- **Track Validation**: Filters out short or unreliable tracks

### 4. Technical Implementation
- **Input**: Images (JPG/PNG) or YOLO pose detection results (bounding boxes + keypoints)
- **Pose Model**: YOLO11m-pose (97% mAP50) from Task 2
- **Output**: Continuous trajectories with consistent IDs and pose information
- **Frame Rate**: 30 FPS processing capability
- **Memory**: Efficient track state management

## File Structure
```
Task3_FlyTracking/
├── README.md                           # This documentation
├── scripts/                           # Core Python scripts
│   ├── fly_tracker.py                 # Main tracking implementation
│   ├── run_integrated_tracking.py     # Integrated tracking with Task 2
│   └── run_behavioral_analysis.py     # Behavioral analysis
├── configs/
│   └── tracking_config.yaml           # Configuration parameters
└── results/                           # Analysis outputs
    ├── analysis_report.md             # Comprehensive analysis report
    ├── final_report.json              # Complete results summary
    ├── tracking_results/              # Fresh tracking data
    │   ├── tracks_summary.csv         # 8,847 tracks
    │   ├── trajectories.csv           # 1,126,902 detections
    │   ├── frames_summary.csv         # 240 frames
    │   └── tracking_stats.json        # Statistics
    └── behavioral_analysis/           # Fresh behavioral data
        ├── behavioral_metrics.csv     # 8,847 tracks metrics
        └── behavioral_summary.json     # Summary statistics
```

## Quick Start

### 1. Integrated Tracking 
```bash
# Run integrated tracking with Task 2 pose results
python scripts/run_integrated_tracking.py

# With custom parameters
python scripts/run_integrated_tracking.py \
    --data_dir /path/to/pose_labels \
    --output_dir /path/to/output \
    --max_disappeared 15 \
    --max_distance 0.15
```

### 2. Behavioral Analysis
```bash
# Run behavioral analysis on tracking results
python scripts/run_behavioral_analysis.py

# With custom directories
python scripts/run_behavioral_analysis.py \
    --tracking_dir results/tracking_results \
    --output_dir results/behavioral_analysis
```

## Results Summary

### Tracking Performance
- **Total Tracks Generated**: 8,847 tracks 
- **Active Tracks**: 7,985 tracks (90.3%) 
- **Average Track Length**: 127.38 frames 
- **Longest Track**: 240 frames 
- **Track Continuity**: 99.7% 
- **Valid Tracks**: 8,847 (100% ≥5 frames) 

### Behavioral Metrics
- **Average Distance**: 3.19 ± 1.55 pixels
- **Average Speed**: 0.78 ± 0.14 pixels/frame
- **Activity Level**: 73.18% ± 10.42% (high activity)
- **Movement Frequency**: 18.70 ± 9.09 bouts per track
- **Time in Center**: 28.34% ± 20.74%
- **Time in Edge**: 71.66% ± 20.74% 

## Configuration

### Key Parameters
```yaml
max_disappeared: 15          # Frames to maintain missing track
max_distance: 0.15           # Max distance for association
pose_weight: 0.7             # Weight for pose similarity
bbox_weight: 0.3             # Weight for bbox similarity
min_track_length: 5          # Minimum frames for valid track
```

### Customization
- Adjust `pose_weight` vs `bbox_weight` for different tracking strategies
- Modify `max_disappeared` for occlusion handling
- Change `max_distance` for association sensitivity


### Performance Optimization
- Use efficient data structures
- Limit maximum track count
- Process frames in batches
- Vectorize distance calculations


## Dependencies
- ultralytics (YOLO)
- opencv-python
- numpy
- pandas
- scipy (Hungarian algorithm)
- matplotlib (visualization)


---

**Task 3 Status**: ✅ **COMPLETE** - Clean, organized, and ready for use

**Key Achievement**: Generated 8,847 continuous behavioral trajectories with 99.7% track continuity, successfully meeting the objective of tracking individual flies across frames.
