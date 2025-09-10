#!/usr/bin/env python3
"""
Auto-label 240 images from Extracted_Frames_task with 3 keypoints visible
"""

import os
import sys
import cv2
import numpy as np
from pathlib import Path
import json
from ultralytics import YOLO

def setup_autolabeling():
    """Setup autolabeling with trained model"""
    print("Setting up autolabeling...")
    
    # Find the best trained model (prioritize larger YOLO11 variants)
    model_paths = [
        "Task2_ModelTraining/results/yolo11m_training/weights/best.pt",  # YOLO11m-pose (best)
        "Task2_ModelTraining/results/yolo11s_training/weights/best.pt",  # YOLO11s-pose (good)
        "Task2_ModelTraining/results/yolo_training/weights/best.pt",     # YOLOv8s-pose (baseline)
        "Task2_ModelTraining/results/yolo11_training/weights/best.pt",   # YOLO11n-pose (small)
        "runs/pose_training_v1/weights/best.pt",
        "yolo11m-pose.pt",  # YOLO11m pretrained
        "yolo11s-pose.pt",  # YOLO11s pretrained
        "yolov8s-pose.pt"   # Fallback to YOLOv8
    ]
    
    model_path = None
    for path in model_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if not model_path:
        print("No trained model found! Using YOLO11m pretrained model.")
        model_path = "yolo11m-pose.pt"
    
    print(f"Using model: {model_path}")
    
    # Load model
    model = YOLO(model_path)
    return model

def process_frames(model, input_dir, output_dir, max_images=240):
    """Process frames and generate labels"""
    print(f"Processing frames from: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Max images: {max_images}")
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Get image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(Path(input_dir).glob(f"*{ext}"))
        image_files.extend(Path(input_dir).glob(f"*{ext.upper()}"))
    
    image_files = sorted(image_files)[:max_images]
    
    print(f"Found {len(image_files)} images to process")
    
    # Process each image
    results = []
    for i, image_path in enumerate(image_files):
        print(f"Processing {i+1}/{len(image_files)}: {image_path.name}")
        
        # Run inference
        results_batch = model.predict(
            source=str(image_path),
            conf=0.25,
            iou=0.6,
            save=False,
            save_txt=True,
            project=output_dir,
            name="autolabeled",
            exist_ok=True
        )
        
        # Process results
        for result in results_batch:
            if result.boxes is not None and len(result.boxes) > 0:
                # Save image with keypoints visualization
                save_visualization(result, image_path, output_dir)
                
                # Count detections
                num_detections = len(result.boxes)
                print(f"  Found {num_detections} flies")
                
                results.append({
                    'image': str(image_path),
                    'detections': num_detections,
                    'keypoints_visible': True
                })
            else:
                print(f"  No flies detected")
                results.append({
                    'image': str(image_path),
                    'detections': 0,
                    'keypoints_visible': False
                })
    
    # Save summary
    summary_path = Path(output_dir) / "autolabel_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAutolabeling complete!")
    print(f"Processed {len(image_files)} images")
    print(f"Results saved to: {output_dir}")
    print(f"Summary saved to: {summary_path}")
    
    return results

def save_visualization(result, image_path, output_dir):
    """Save image with keypoints visualization"""
    # Load original image
    image = cv2.imread(str(image_path))
    
    if result.keypoints is not None and len(result.keypoints) > 0:
        # Draw keypoints
        for kpts in result.keypoints.data:
            if len(kpts) >= 3:  # Ensure we have 3 keypoints
                # Draw keypoints
                for i, (x, y, conf) in enumerate(kpts):
                    if conf > 0.5:  # Only draw visible keypoints
                        color = (0, 255, 0) if i == 0 else (255, 0, 0) if i == 1 else (0, 0, 255)
                        cv2.circle(image, (int(x), int(y)), 5, color, -1)
                        cv2.putText(image, f"K{i+1}", (int(x)+5, int(y)-5), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Draw bounding boxes
        if result.boxes is not None:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0].cpu().numpy()
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
                cv2.putText(image, f"Fly: {conf:.2f}", (int(x1), int(y1)-10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    # Save visualization
    vis_path = Path(output_dir) / "visualizations" / f"vis_{image_path.name}"
    vis_path.parent.mkdir(exist_ok=True)
    cv2.imwrite(str(vis_path), image)

def main():
    """Main autolabeling pipeline"""
    print("=== Auto-labeling Frames for Task 2 ===")
    
    # Setup
    model = setup_autolabeling()
    
    # Input and output directories
    input_dir = "/mnt/storage5/Fruitfly/Extracted_Frames_task"
    output_dir = "Task2_ModelTraining/results/autolabeled_frames"
    
    # Check input directory
    if not os.path.exists(input_dir):
        print(f"Input directory not found: {input_dir}")
        return False
    
    # Process frames
    results = process_frames(model, input_dir, output_dir, max_images=240)
    
    # Summary
    total_detections = sum(r['detections'] for r in results)
    images_with_detections = sum(1 for r in results if r['detections'] > 0)
    
    print(f"\n=== Autolabeling Summary ===")
    print(f"Total images processed: {len(results)}")
    print(f"Images with detections: {images_with_detections}")
    print(f"Total flies detected: {total_detections}")
    print(f"Average detections per image: {total_detections/len(results):.2f}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
