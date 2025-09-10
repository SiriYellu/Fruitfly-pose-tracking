# Video Data Summary

## 🎥 **Video Data Overview**

### **Data Statistics**
- **Total Video Files**: 147 videos
- **Valid Videos**: 144 videos (97.96% success rate)
- **Corrupted Videos**: 3 videos (img0048 from each date)
- **Total Duration**: 4,320.7 minutes (72 hours)
- **Total Frames**: 7,776,000 frames
- **Resolution**: 2448x2048 pixels
- **Frame Rate**: 30 FPS
- **File Size**: ~2.6 GB compressed

### **Data Organization**
```
Data_Preparation/
├── FlyData/                          # Original video files
│   ├── run 231020/                   # October 20, 2023 (48 videos)
│   ├── run 231106/                   # November 6, 2023 (48 videos)  
│   └── run 231127/                   # November 27, 2023 (48 videos)
├── extracted_frames/                 # Sample frames for pose estimation
│   ├── FVI_20231020_184807_img0000_frame_000000.jpg
│   ├── FVI_20231020_184807_img0000_frame_000300.jpg
│   └── ... (8 frames extracted so far)
├── data_summary.json                 # Detailed data statistics
└── processing_report.json            # Frame extraction report
```

### **Video File Naming Convention**
- **Format**: `FVI_YYYYMMDD_HHMMSS_imgXXXX.mp4`
- **Example**: `FVI_20231020_184807_img0000.mp4`
- **Date**: YYYYMMDD (20231020 = October 20, 2023)
- **Time**: HHMMSS (184807 = 6:48:07 PM)
- **Image ID**: XXXX (0000-0047 for each date)

### **Video Content Analysis**
- **Duration per Video**: 30 minutes (1,800 seconds)
- **Frames per Video**: 54,000 frames
- **Resolution**: 2448x2048 (4K quality)
- **Aspect Ratio**: 1.2:1 (slightly wider than square)
- **File Size**: ~18-25 MB per video

## 📊 **Data Quality Assessment**

### **✅ Strengths**
- **High Resolution**: 2448x2048 provides excellent detail for fly detection
- **Consistent Format**: All videos have identical specifications
- **Long Duration**: 30-minute recordings capture extended behavior
- **High Frame Rate**: 30 FPS enables smooth motion analysis
- **Good Coverage**: 3 different dates for temporal analysis

### **⚠️ Issues Identified**
- **3 Corrupted Files**: img0048 from each date (2% failure rate)
- **Large File Size**: 7.7M frames require significant processing power
- **Storage Requirements**: Full processing would need ~500GB+ storage

## 🚀 **Recommended Processing Strategy**

### **Phase 1: Sample Analysis (Current)**
- Extract 10 frames per video (every 300th frame)
- Total: ~1,440 frames for initial pose estimation
- Purpose: Model training and validation

### **Phase 2: Representative Analysis**
- Extract 50 frames per video (every 60th frame)
- Total: ~7,200 frames for comprehensive analysis
- Purpose: Full behavioral analysis

### **Phase 3: Full Analysis (Optional)**
- Process all 7.7M frames
- Requires significant computational resources
- Purpose: Complete temporal analysis

## 🛠️ **Next Steps**

### **Immediate Actions**
1. **Complete Frame Extraction**: Extract more frames for pose estimation
2. **Run Pose Estimation**: Use extracted frames to train pose models
3. **Validate Results**: Check pose detection quality on sample frames

### **Commands to Run**
```bash
# Extract more frames (50 per video)
python Data_Preparation/process_video_data.py --frame_interval 60 --max_frames 50

# Run pose estimation on extracted frames
python run_tracking_pipeline.py --data_dir Data_Preparation/extracted_frames --output_dir Results/video_analysis

# Validate pose detection quality
python Task1_PoseEstimation/scripts/evaluate_pose.py --data_dir Data_Preparation/extracted_frames
```

### **Expected Outcomes**
- **Pose Detection**: Detect fly keypoints in video frames
- **Tracking**: Track flies across video sequences
- **Behavioral Analysis**: Extract movement patterns and behaviors
- **Statistical Analysis**: Compare behaviors across different dates

## 📈 **Computational Requirements**

### **Storage Needs**
- **Raw Videos**: 2.6 GB (compressed)
- **Extracted Frames**: ~500 MB (1,440 frames)
- **Pose Annotations**: ~50 MB
- **Tracking Results**: ~100 MB
- **Total**: ~3.2 GB

### **Processing Time Estimates**
- **Frame Extraction**: 2-3 hours (1,440 frames)
- **Pose Estimation**: 1-2 hours (1,440 frames)
- **Tracking**: 30 minutes (1,440 frames)
- **Behavioral Analysis**: 15 minutes
- **Total**: 4-6 hours

### **Hardware Requirements**
- **GPU**: 4x NVIDIA L40 (available)
- **RAM**: 32GB+ recommended
- **Storage**: 10GB+ free space
- **CPU**: Multi-core recommended

## 🔬 **Research Applications**

### **Temporal Analysis**
- Compare behavior across 3 different dates
- Analyze long-term behavioral patterns
- Study circadian rhythms (different times of day)

### **Spatial Analysis**
- Track fly movement within vials
- Analyze spatial preferences
- Study interaction patterns

### **Behavioral Analysis**
- Quantify movement patterns
- Analyze activity levels
- Study social behaviors

## 📋 **Data Management**

### **File Organization**
- Keep original videos in `FlyData/`
- Store extracted frames in `extracted_frames/`
- Save results in `Results/`
- Maintain processing logs

### **Backup Strategy**
- Original videos are safely stored
- Processing results can be regenerated
- Keep intermediate results for debugging

## 🎯 **Success Metrics**

### **Technical Metrics**
- **Pose Detection Accuracy**: >85% mAP@0.5
- **Tracking Continuity**: >90% track continuity
- **Processing Speed**: >30 FPS
- **Data Quality**: >95% valid frames

### **Research Metrics**
- **Behavioral Patterns**: Quantified movement metrics
- **Temporal Trends**: Time-based behavior analysis
- **Spatial Analysis**: Regional occupancy patterns
- **Statistical Significance**: Robust behavioral differences

---

**Last Updated**: September 10, 2025
**Data Source**: 2023 FlyVialImage_Data
**Status**: Ready for pose estimation and tracking analysis
