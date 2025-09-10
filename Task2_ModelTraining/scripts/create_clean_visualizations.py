#!/usr/bin/env python3
"""
Create Clean Visualizations Script
Generates images with only flies and skeletons (keypoints) without bounding boxes
"""

import cv2
import numpy as np
import os
import json
from pathlib import Path
from ultralytics import YOLO

def create_clean_visualization(image_path, label_path, output_path, model_path):
    """Create clean visualization with only flies and skeletons"""
    
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not load image: {image_path}")
        return False
    
    # Load model for pose detection
    model = YOLO(model_path)
    
    # Run inference
    results = model(image, conf=0.25)
    
    # Create clean visualization
    clean_image = image.copy()
    
    # Define colors for keypoints (BGR format)
    keypoint_colors = [
        (0, 255, 0),    # Green for head
        (255, 0, 0),    # Blue for thorax  
        (0, 0, 255)     # Red for abdomen
    ]
    
    # Define skeleton connections
    skeleton = [(0, 1), (1, 2)]  # head-thorax, thorax-abdomen
    
    for result in results:
        if result.keypoints is not None and len(result.keypoints.data) > 0:
            # Process each detection
            for detection_keypoints in result.keypoints.data:
                if detection_keypoints is not None and len(detection_keypoints) >= 3:
                    # Draw skeleton lines first
                    for connection in skeleton:
                        pt1_idx, pt2_idx = connection
                        if pt1_idx < len(detection_keypoints) and pt2_idx < len(detection_keypoints):
                            pt1 = detection_keypoints[pt1_idx]
                            pt2 = detection_keypoints[pt2_idx]
                            
                            # Check if both points are visible (confidence > 0)
                            if len(pt1) >= 3 and len(pt2) >= 3 and pt1[2] > 0 and pt2[2] > 0:
                                x1, y1 = int(pt1[0]), int(pt1[1])
                                x2, y2 = int(pt2[0]), int(pt2[1])
                                # Draw thick white skeleton line
                                cv2.line(clean_image, (x1, y1), (x2, y2), (255, 255, 255), 3)
                    
                    # Draw keypoints
                    for i, keypoint in enumerate(detection_keypoints):
                        if len(keypoint) >= 3 and keypoint[2] > 0:  # Check visibility
                            x, y = int(keypoint[0]), int(keypoint[1])
                            color = keypoint_colors[i % len(keypoint_colors)]
                            # Draw larger, more visible keypoints
                            cv2.circle(clean_image, (x, y), 6, color, -1)
                            cv2.circle(clean_image, (x, y), 8, (255, 255, 255), 2)
    
    # Save clean visualization
    cv2.imwrite(output_path, clean_image)
    return True

def main():
    """Main function to create clean visualizations"""
    
    print("Creating clean visualizations with flies and skeletons only...")
    
    # Paths
    base_dir = Path("Task2_ModelTraining/results/autolabeled_frames")
    input_images_dir = Path("Extracted_Frames_task")
    output_dir = base_dir / "clean_visualizations"
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Find best model
    model_paths = [
        "Task2_ModelTraining/results/yolo11m_training/weights/best.pt",
        "Task2_ModelTraining/results/yolo11s_training/weights/best.pt", 
        "Task2_ModelTraining/results/yolo_training/weights/best.pt",
        "yolo11m-pose.pt"
    ]
    
    model_path = None
    for path in model_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if not model_path:
        print("No trained model found!")
        return
    
    print(f"Using model: {model_path}")
    
    # Get all image files
    image_files = list(input_images_dir.glob("*.jpg"))
    print(f"Found {len(image_files)} images to process")
    
    # Process each image
    processed = 0
    for image_file in image_files:
        try:
            # Create output filename
            output_file = output_dir / f"clean_{image_file.name}"
            
            # Create clean visualization
            success = create_clean_visualization(
                str(image_file), 
                None,  # We don't need label files for this
                str(output_file),
                model_path
            )
            
            if success:
                processed += 1
                if processed % 50 == 0:
                    print(f"Processed {processed}/{len(image_files)} images...")
        
        except Exception as e:
            print(f"Error processing {image_file}: {e}")
    
    print(f"\n✅ Clean visualizations complete!")
    print(f"Processed: {processed}/{len(image_files)} images")
    print(f"Output directory: {output_dir}")
    print(f"Images contain: Flies with skeletons (3 keypoints) - NO bounding boxes")

if __name__ == "__main__":
    main()
