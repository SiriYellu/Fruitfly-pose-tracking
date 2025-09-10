# Task 2: Model Training - Fruit Fly Pose Estimation

##  **Objective**
Train state-of-the-art YOLO pose estimation models on Roboflow fruit fly dataset and auto-label 240 images with 3 keypoints (head, thorax, abdomen) clearly visible.

##  **Key Findings & Results**

###  **Best Performing Model: YOLO11m-pose**
- **Pose mAP50**: 97.0% (highest accuracy)
- **Pose mAP50-95**: 89.8% (excellent precision)
- **Box mAP50**: 95.3% (superior detection)
- **Model Size**: 42.2MB
- **Parameters**: 20.9M
- **Training Time**: 0.031 hours (100 epochs)

###  **Model Performance Comparison**
| Model | Pose mAP50 | Pose mAP50-95 | Box mAP50 | Model Size | Parameters | Status |
|-------|------------|---------------|-----------|------------|------------|--------|
| **YOLO11m-pose** | **97.0%** | **89.8%** | **95.3%** | 42.2MB | 20.9M | ✅ **BEST** |
| YOLO11s-pose | 96.9% | 89.7% | 95.2% | 18.9MB | ~9M | ✅ Good |
| YOLOv8s-pose | 96.7% | 78.6% | 91.6% | 23.1MB | 11.4M | ✅ Baseline |
| YOLO11n-pose | 95.1% | 64.0% | 84.9% | 5.6MB | 2.7M | ✅ Fast |

###  **Auto-labeling Results**
- ** Images Processed**: 240/240 (100% success rate)
- ** Total Flies Detected**: 15,701 flies
- ** Average per Image**: 65.42 flies per image
- ** Processing Speed**: ~6.5ms per image
- ** Keypoints**: 3 per fly (Head 🟢, Thorax 🔵, Abdomen 🔴)

##  **Directory Structure**

```
Task2_ModelTraining/
├── 📁 configs/                           # Configuration files
│   ├── training_config.yaml             # YOLO training parameters
│   └── autolabel_config.yaml            # Auto-labeling settings
├── 📁 datasets/                          # Dataset management
│   ├── train/                           # Training images (18 images)
│   ├── valid/                           # Validation images (6 images)
│   └── test/                            # Test images (6 images)
├── 📁 examples/                          # Usage examples
│   └── sample_usage.py                  # Example code
├── 📁 models/                            # Model files
│   ├── yolo11m-pose.pt                  # Best model (42.2MB)
│   ├── yolo11s-pose.pt                  # Small variant (18.9MB)
│   ├── yolo11n-pose.pt                  # Nano variant (5.6MB)
│   └── yolov8s-pose.pt                  # Baseline model (23.1MB)
├── 📁 results/                           # All training and annotation results
│   ├── 📁 autolabeled_frames/           # 240 annotated images
│   │   ├── 📁 autolabeled/
│   │   │   ├── 📁 labels/               # 240 YOLO format label files
│   │   │   └── 📁 images/               # Original images (to be created)
│   │   ├── 📁 visualizations/           # 240 images with bounding boxes
│   │   ├── 📁 clean_visualizations/     # 240 images with skeletons only
│   │   └── 📄 autolabel_summary.json    # Complete statistics
│   ├── 📁 yolo_training/                # YOLOv8s-pose results
│   ├── 📁 yolo11_training/              # YOLO11n-pose results
│   ├── 📁 yolo11s_training/             # YOLO11s-pose results
│   └── 📁 yolo11m_training/             # YOLO11m-pose results (BEST)
├── 📁 scripts/                           # All training and annotation scripts
│   ├── download_dataset.py              # Roboflow dataset downloader
│   ├── train_yolo.py                    # Single model training
│   ├── train_yolo11_models.py           # Multi-model training
│   ├── autolabel_frames.py              # Auto-labeling script
│   ├── create_clean_visualizations.py   # Clean skeleton visualizations
│   └── run_task2_pipeline.py            # End-to-end pipeline
├── 📁 test/                              # Test dataset (6 images)
├── 📁 train/                             # Training dataset (18 images)
├── 📁 valid/                             # Validation dataset (6 images)
├── 📄 data.yaml                          # Dataset configuration
├── 📄 README.md                          # This documentation
├── 📄 TASK2_SUMMARY.md                   # Task 2 summary
├── 📄 YOLO11_TRAINING_PLAN.md            # Training strategy
└── 📄 *.pt                               # Model weight files
```

##  **Quick Start**

### 1. **Download Dataset**
```bash
cd Task2_ModelTraining
python scripts/download_dataset.py
```

### 2. **Train Models**
```bash
# Train all YOLO11 variants
python scripts/train_yolo11_models.py

# Or train single model
python scripts/train_yolo.py
```

### 3. **Auto-label Images**
```bash
python scripts/autolabel_frames.py
```

### 4. **Create Clean Visualizations**
```bash
python scripts/create_clean_visualizations.py
```

##  **Input Data**

### **Roboflow Dataset**
- **Source**: [Fruit Fly Pose Tracking Dataset](https://universe.roboflow.com/2023-flyviallmagedata/fruit-fly-pose-tracking-rrhal/dataset/3)
- **Total Images**: 30 images
- **Annotations**: 5,592 keypoint annotations
- **Format**: YOLO pose format
- **Keypoints**: 3 per fly (head, thorax, abdomen)
- **Split**: 18 train, 6 validation, 6 test

### **Target Images for Auto-labeling**
- **Source**: `/mnt/storage5/Fruitfly/Extracted_Frames_task/`
- **Total Images**: 240 images
- **Format**: JPG
- **Resolution**: Various (resized to 640x640 for processing)

##  **Technical Details**

### **Training Configuration**
```yaml
# YOLO11 Optimized Settings
epochs: 100
imgsz: 640
batch: 16
device: 0
optimizer: 'AdamW'
lr0: 0.001
weight_decay: 0.0005
warmup_epochs: 3
cos_lr: True
close_mosaic: 10

# Advanced Augmentation
hsv_h: 0.015
hsv_s: 0.7
hsv_v: 0.4
degrees: 0.0
translate: 0.1
scale: 0.5
shear: 0.0
perspective: 0.0
flipud: 0.0
fliplr: 0.5
mosaic: 1.0
mixup: 0.0
```

### **Keypoint Configuration**
```yaml
kpt_shape: [3, 3]  # 3 keypoints, 3 values each (x, y, visibility)
flip_idx: [0, 1, 2]  # All keypoints can be flipped
nc: 1  # Number of classes
names: ['Fruitfly']  # Class name
```

### **Keypoint Mapping**
- **Index 0**: Head (🟢 Green)
- **Index 1**: Thorax (🔵 Blue)
- **Index 2**: Abdomen (🔴 Red)

##  **Output Files**

### **1. Trained Models**
- `yolo11m_training/weights/best.pt` - Best performing model
- `yolo11s_training/weights/best.pt` - Small variant
- `yolo_training/weights/best.pt` - YOLOv8s baseline

### **2. Auto-labeled Data**
- `autolabeled_frames/autolabeled/labels/` - 240 YOLO format label files
- `autolabeled_frames/visualizations/` - Images with bounding boxes
- `autolabeled_frames/clean_visualizations/` - Images with skeletons only

### **3. Training Results**
- `results/*/weights/` - Model weights
- `results/*/results.png` - Training curves
- `results/*/confusion_matrix.png` - Confusion matrices
- `results/*/val_batch*.jpg` - Validation samples

##  **Visualization Types**

### **1. Standard Visualizations** (`visualizations/`)
- Original images with bounding boxes
- Keypoints with confidence scores
- Class labels and detection confidence

### **2. Clean Visualizations** (`clean_visualizations/`)
- Original images with skeletons only
- No bounding boxes
- Clear keypoint connections
- Color-coded keypoints (Head=Green, Thorax=Blue, Abdomen=Red)

## 📈 **Performance Metrics**

### **Training Metrics**
- **Box Loss**: 1.685 (final epoch)
- **Pose Loss**: 0.5385 (final epoch)
- **Classification Loss**: 0.7238 (final epoch)
- **DFL Loss**: 0.868 (final epoch)

### **Validation Metrics**
- **Precision**: 89.5%
- **Recall**: 94.4%
- **mAP50**: 97.0%
- **mAP50-95**: 89.8%

##  **Key Insights**

### **1. Model Architecture Impact**
- **YOLO11m-pose** achieved the best balance of accuracy and performance
- **YOLO11n-pose** was too small for complex pose estimation
- **YOLO11s-pose** provided good accuracy with smaller size

### **2. Training Optimization**
- **AdamW optimizer** with cosine learning rate scheduling
- **Advanced augmentation** significantly improved generalization
- **Mosaic augmentation** helped with multi-fly scenarios

### **3. Pose Estimation Quality**
- **97% mAP50** indicates excellent keypoint detection
- **89.8% mAP50-95** shows high precision across IoU thresholds
- **Consistent performance** across different fly densities

##  **Dependencies**

```bash
# Core dependencies
ultralytics>=8.3.197
opencv-python>=4.8.0
numpy>=1.24.0
torch>=2.0.0
torchvision>=0.15.0

# Additional dependencies
matplotlib>=3.7.0
pillow>=9.5.0
pyyaml>=6.0
```

##  **Usage Examples**

### **Load Best Model**
```python
from ultralytics import YOLO

# Load the best performing model
model = YOLO('Task2_ModelTraining/results/yolo11m_training/weights/best.pt')

# Run inference
results = model('path/to/image.jpg')

# Access keypoints
for result in results:
    if result.keypoints is not None:
        keypoints = result.keypoints.data[0]  # First detection
        for i, kpt in enumerate(keypoints):
            x, y, conf = kpt[0], kpt[1], kpt[2]
            print(f"Keypoint {i}: ({x:.2f}, {y:.2f}) conf={conf:.3f}")
```

### **Batch Processing**
```python
# Process multiple images
results = model(['image1.jpg', 'image2.jpg', 'image3.jpg'])

# Save results
for i, result in enumerate(results):
    result.save(f'output_{i}.jpg')
```

##  **Success Criteria Met**

-  **Dataset downloaded** from Roboflow (30 images, 5,592 annotations)
-  **Multiple models trained** (YOLO11n, YOLO11s, YOLO11m, YOLOv8s)
-  **Best model selected** (YOLO11m-pose with 97% mAP50)
-  **240 images auto-labeled** with 3 keypoints visible
-  **Clean visualizations created** with skeletons only
-  **High-quality annotations** (15,701 flies detected)
-  **Comprehensive documentation** and organized structure

##  **Support**

For questions or issues:
1. Check the `TASK2_SUMMARY.md` for quick overview
2. Review the `YOLO11_TRAINING_PLAN.md` for technical details
3. Examine the example scripts in `examples/` folder
4. Refer to the Ultralytics documentation for YOLO usage

---

*Generated on: $(date)*
*Total Processing Time: ~2 hours*
*Models Trained: 4*
*Images Processed: 240*
*Flies Detected: 15,701*
