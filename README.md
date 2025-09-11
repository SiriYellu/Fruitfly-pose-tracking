# Fruit Fly Pose Tracking Project

## Overview
This repository contains a comprehensive fruit fly pose tracking system with multiple tasks focusing on data preparation, model training, and behavioral analysis. The project uses YOLO-based architectures for detecting and localizing key anatomical points (head, thorax, abdomen) on individual flies in video frames.

## Project Structure

```
Fruitfly-pose-tracking/
├── README.md                                    # This file
├── Task1_PoseEstimation/                        # Task 1: Data preparation and frame extraction
│   ├── README.md
│   ├── extract_5_per_recording.py
│   ├── Data_Preparation/
│   ├── Extracted_Frames_task/
│   ├── samples/
│   └── Fruit Fly Pose Tracking.v3i.yolov8 (2).zip
├── Task2_ModelTraining/                         # Task 2: YOLO model training and pose estimation
│   ├── README.md
│   ├── TASK2_SUMMARY.md
│   ├── YOLO11_TRAINING_PLAN.md
│   ├── configs/
│   ├── scripts/
│   ├── train/
│   ├── valid/
│   ├── test/
│   └── models/
├── Task3_FlyTracking/                           # Task 3: Fly tracking and behavioral analysis
│   ├── README.md
│   ├── TASK3_SUMMARY.md
│   ├── fly_tracker.py
│   ├── behavioral_analyzer.py
│   ├── run_tracking_pipeline.py
│   ├── configs/
│   ├── scripts/
│   └── results/
└── Task4_BehavioralAnalysis/                    # Task 4: Comprehensive behavioral analysis
    ├── README.md
    ├── behavioral_analyzer.py
    ├── run_behavioral_analysis.py
    ├── scripts/
    ├── visualizations/
    └── results/
```

## Current Project Status

### Task 1: Pose Estimation Model Development
- **Data Preparation**: ✅ Complete
- **Frame Extraction**: ✅ Complete (240 frames extracted)
- **Model Training**: ⏳ Pending
- **Pose Estimation**: ⏳ Pending

### Task 2: Model Training
- **Dataset Preparation**: ✅ Complete (annotated dataset with train/valid/test splits)
- **Model Files**: ✅ Complete (YOLO11 and YOLOv8 models)
- **Training Scripts**: ✅ Complete
- **Configuration**: ✅ Complete

### Task 3: Fly Tracking
- **Tracking Pipeline**: ✅ Complete (pose-based tracking system)
- **Behavioral Analysis**: ✅ Complete (movement and behavior analysis)
- **Integration Scripts**: ✅ Complete
- **Results Processing**: ✅ Complete

### Task 4: Behavioral Analysis
- **Advanced Analytics**: ✅ Complete (comprehensive behavioral analysis)
- **Visualization Tools**: ✅ Complete (research dashboards and charts)
- **Statistical Analysis**: ✅ Complete (clustering and correlation analysis)
- **Research Outputs**: ✅ Complete (publication-ready visualizations)

## Project Structure

```
Task1_PoseEstimation/
├── README.md                                    # This file
├── extract_5_per_recording.py                  # Frame extraction script
├── Extracted_Frames_task/                      # Extracted sample frames (240 frames)
│   ├── run_231020_seg000_frame41934.jpg
│   ├── run_231020_seg001_frame1668.jpg
│   └── ... (240 total frames)
├── Data_Preparation/                           # Data preparation pipeline
│   ├── README.md                              # Data preparation documentation
│   ├── data_summary.json                      # Video data statistics
│   ├── VIDEO_DATA_SUMMARY.md                  # Detailed data analysis
│   ├── create_download_tools.py               # Download utility creation
│   ├── download_video_data.py                 # Video data download script
│   ├── process_video_data.py                  # Video processing pipeline
│   ├── setup_download_tools.py                # Setup download tools
│   ├── validate_video_data.py                 # Data validation script
│   ├── prepare_windows_data.bat               # Windows batch processing
│   ├── transfer_commands.txt                  # Data transfer commands
│   ├── fly_video_data.tar.gz                  # Compressed video data (2.6GB)
│   ├── extracted_frames/                      # Additional extracted frames
│   └── FlyData/                               # Original video files
│       ├── run 231020/                        # October 20, 2023 (48 videos)
│       ├── run 231106/                        # November 6, 2023 (48 videos)
│       └── run 231127/                        # November 27, 2023 (48 videos)
└── Fruit Fly Pose Tracking.v3i.yolov8 (2).zip # Roboflow dataset (compressed)
```

## Task 2: Model Training Overview

### Dataset Information
- **Annotated Dataset**: Complete YOLO format dataset with pose annotations
- **Train/Valid/Test Split**: Properly divided dataset for model training
- **Keypoints**: 3 anatomical points per fly (head, thorax, abdomen)
- **Model Files**: Pre-trained YOLO models included
  - `yolo11n-pose.pt` (6.3 MB)
  - `yolo11m-pose.pt` (42.5 MB) 
  - `yolo11s-pose.pt` (20.4 MB)
  - `yolov8s-pose.pt` (23.5 MB)

### Training Scripts
- **train_yolo.py**: YOLO model training script
- **train_yolo11_models.py**: YOLO11 specific training
- **autolabel_frames.py**: Automatic frame labeling
- **run_task2_pipeline.py**: Complete training pipeline

### Configuration Files
- **training_config.yaml**: Training parameters and hyperparameters
- **autolabel_config.yaml**: Auto-labeling configuration
- **data.yaml**: Dataset configuration

## Task 3: Fly Tracking Overview

### Tracking System
- **Pose-Based Tracking**: Advanced tracking using pose estimation results
- **Multi-Object Tracking**: Handles multiple flies simultaneously
- **Trajectory Analysis**: Complete movement path reconstruction
- **Behavioral Classification**: Automatic behavior pattern recognition

### Key Features
- **Real-time Processing**: Efficient tracking pipeline
- **Data Integration**: Seamless integration with pose estimation
- **Result Export**: Multiple output formats for analysis
- **Visualization**: Interactive tracking visualizations

## Task 4: Behavioral Analysis Overview

### Analysis Capabilities
- **Movement Analysis**: Speed, acceleration, and trajectory analysis
- **Spatial Behavior**: Regional occupancy and preference analysis
- **Temporal Patterns**: Time-series behavioral analysis
- **Statistical Analysis**: Advanced statistical modeling and clustering

### Visualization Tools
- **Research Dashboards**: Publication-ready visualizations
- **Behavioral Clusters**: Automated behavior pattern identification
- **Correlation Analysis**: Behavioral correlation matrices
- **Enhanced Visualizations**: Multi-dimensional behavioral insights

## Task 1: Data Overview

### Video Data Statistics
- **Total Video Files**: 147 videos (144 valid, 3 corrupted)
- **Total Duration**: 4,320.7 minutes (72 hours)
- **Resolution**: 2448x2048 pixels (4K quality)
- **Frame Rate**: 30 FPS
- **Recording Dates**: October 20, November 6, and November 27, 2023
- **Videos per Date**: 48 videos (30 minutes each)
- **File Size**: 2.6 GB compressed

### Extracted Frames
- **Sample Frames**: 240 frames extracted using `extract_5_per_recording.py`
- **Extraction Strategy**: 80 frames per recording run (3 runs × 80 = 240 total)
- **Frame Selection**: Random sampling with 1-second margin from video start/end
- **Naming Convention**: `{run_date}_seg{segment:03d}_frame{frame_number}.jpg`
- **File Sizes**: ~250-290 KB per frame

## Data Preparation Pipeline

### 1. Video Data Processing
The data preparation pipeline processes raw video files from the 2023 FlyVialImage_Data collection:

```json
{
  "total_videos": 147,
  "valid_videos": 144,
  "total_duration_minutes": 4320.72,
  "total_frames": 7776000,
  "resolution_distribution": {"2448x2048": 144},
  "fps_distribution": {"30": 144}
}
```

### 2. Frame Extraction Process
The `extract_5_per_recording.py` script implements intelligent frame extraction:

- **Sampling Strategy**: Evenly distributed across video segments
- **Quality Control**: Skips videos with insufficient frames
- **Randomization**: Uses seed=42 for reproducible results
- **Error Handling**: Robust video opening with retry mechanism
- **Configuration**:
  - `FRAMES_PER_RUN = 80` (frames per recording run)
  - `RANDOM_SEED = 42` (for reproducibility)
  - `VIDEO_EXTS = (".mp4", ".mov", ".avi", ".mkv")`

### 3. Data Validation
Comprehensive validation ensures data quality:
- **File Integrity**: Checks for corrupted video files
- **Frame Quality**: Validates extracted frame quality
- **Temporal Distribution**: Ensures even sampling across video duration

## Available Scripts

### Frame Extraction
```bash
# Extract frames from video recordings
python extract_5_per_recording.py
```

### Data Processing
```bash
# Process video data
python Data_Preparation/process_video_data.py

# Validate video data
python Data_Preparation/validate_video_data.py

# Download video data
python Data_Preparation/download_video_data.py
```

## Next Steps for Pose Estimation

### Phase 1: Model Setup
1. **Environment Setup**:
   ```bash
   # Create virtual environment
   python3 -m venv ~/venvs/flypose
   source ~/venvs/flypose/bin/activate
   
   # Install dependencies
   pip install ultralytics==8.2.77 numpy<2.0
   ```

2. **Data Preparation**:
   - Extract Roboflow dataset from `Fruit Fly Pose Tracking.v3i.yolov8 (2).zip`
   - Prepare YOLO format annotations
   - Configure data.yaml with correct keypoint shape

### Phase 2: Model Training
1. **Model Selection**: Choose YOLO pose estimation model (YOLOv8-Pose or YOLOv11-Pose)
2. **Training Configuration**:
   ```yaml
   # Model Parameters
   model: yolov8s-pose.pt
   epochs: 100
   batch_size: 24 (4 GPUs) / 16 (2 GPUs) / 8 (1 GPU)
   imgsz: 640
   device: 0,1,2,3 (multi-GPU) / 0 (single GPU)
   
   # Data Augmentation
   mosaic: 0.0
   degrees: 10
   translate: 0.05
   scale: 0.15
   shear: 0.0
   fliplr: 0.5
   flipud: 0.0
   hsv_h: 0.015
   hsv_s: 0.7
   hsv_v: 0.4
   
   # Training Parameters
   patience: 20
   workers: 16
   seed: 42
   ```

3. **Training Command**:
   ```bash
   yolo pose train \
     --model yolov8s-pose.pt \
     --data data.yaml \
     --imgsz 640 \
     --epochs 100 \
     --batch 24 \
     --device 0,1,2,3 \
     --workers 16 \
     --patience 20 \
     --project runs \
     --name pose_training_v1
   ```

### Phase 3: Model Evaluation
```bash
# Validate model
yolo pose val \
  --model runs/pose_training_v1/weights/best.pt \
  --data data.yaml \
  --imgsz 640 \
  --batch 16 \
  --device 0 \
  --save_json \
  --project runs \
  --name pose_evaluation_v1
```

## Computational Requirements

### Hardware Requirements
- **GPU**: 4x NVIDIA L40 (available)
- **RAM**: 32GB+ recommended
- **Storage**: 10GB+ free space
- **CPU**: Multi-core recommended

### Processing Time Estimates
- **Frame Extraction**: Complete (240 frames)
- **Pose Estimation**: 1-2 hours (240 frames)
- **Tracking**: 30 minutes (240 frames)
- **Behavioral Analysis**: 15 minutes
- **Total Remaining**: 2-3 hours

## Research Applications

### Temporal Analysis
- Compare behavior across 3 different dates
- Analyze long-term behavioral patterns
- Study circadian rhythms (different times of day)

### Spatial Analysis
- Track fly movement within vials
- Analyze spatial preferences
- Study interaction patterns

### Behavioral Analysis
- Quantify movement patterns
- Analyze activity levels
- Study social behaviors

## Troubleshooting

### Common Issues
1. **Video Access**: Ensure proper file permissions for video files
2. **Frame Quality**: Check extracted frame quality and adjust parameters
3. **Memory Usage**: Monitor RAM usage during processing
4. **File Paths**: Verify correct path configurations in scripts

### Performance Optimization
- Use appropriate batch sizes for available GPU memory
- Enable data loading optimization
- Consider using multiple GPUs for training
- Implement data augmentation strategies

## Success Metrics

### Technical Metrics
- **Frame Extraction**: 100% success rate for valid videos
- **Data Quality**: >95% valid frames
- **Processing Speed**: Efficient frame extraction
- **Storage Efficiency**: Optimized file sizes

### Research Metrics (To Be Achieved)
- **Pose Detection Accuracy**: Target >85% mAP@0.5
- **Tracking Continuity**: Target >90% track continuity
- **Processing Speed**: Target >30 FPS
- **Data Quality**: Target >95% valid frames

---

**Last Updated**: January 2025
**Data Source**: 2023 FlyVialImage_Data
**Status**: Data preparation complete, ready for pose estimation model development