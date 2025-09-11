# Task 2 Sample Results

This directory contains sample results from the Task 2 model training and pose estimation pipeline.

## Sample Images

The following images demonstrate the pose estimation results on fruit fly frames:

### Clean Visualizations
- `clean_run_231020_seg000_frame41934.jpg` - Pose estimation on October 20, 2023 frame
- `clean_run_231020_seg001_frame1668.jpg` - Pose estimation on October 20, 2023 frame  
- `clean_run_231020_seg001_frame7325.jpg` - Pose estimation on October 20, 2023 frame
- `clean_run_231020_seg002_frame18053.jpg` - Pose estimation on October 20, 2023 frame
- `clean_run_231020_seg002_frame48627.jpg` - Pose estimation on October 20, 2023 frame

## Key Features Demonstrated

### Pose Estimation Results
- **Keypoint Detection**: 3 anatomical points per fly (head, thorax, abdomen)
- **Bounding Box Detection**: Accurate fly detection and localization
- **Confidence Scores**: High-confidence pose predictions
- **Multi-Fly Detection**: Handling multiple flies in single frames

### Technical Specifications
- **Model**: YOLO11 and YOLOv8 pose estimation models
- **Resolution**: 2448x2048 pixels (4K quality)
- **Format**: Clean visualization with pose keypoints overlaid
- **Quality**: High-confidence predictions with clear keypoint visibility

## Usage

These sample images can be used for:
- **Model Validation**: Checking pose estimation quality
- **Research Presentations**: Demonstrating system capabilities
- **Quality Assessment**: Evaluating keypoint detection accuracy
- **Documentation**: Visual examples of the system output

## Full Results

The complete results dataset contains:
- **Training Results**: Model training logs and metrics
- **Validation Results**: Performance evaluation on test data
- **Autolabeled Frames**: Full dataset with pose annotations
- **Clean Visualizations**: Publication-ready result images

For access to the complete results, refer to the full Task2_ModelTraining directory.

---

**Generated**: September 2025
**Model**: YOLO11/YOLOv8 Pose Estimation
**Data Source**: 2023 FlyVialImage_Data
