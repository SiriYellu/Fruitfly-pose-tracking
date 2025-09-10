#!/usr/bin/env python3
"""
Train latest YOLO model on Roboflow dataset for Task 2
"""

import os
import sys
import subprocess
from pathlib import Path
import yaml

def install_ultralytics():
    """Install latest ultralytics package"""
    print("Installing latest ultralytics...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "ultralytics", "--upgrade"], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error installing ultralytics: {result.stderr}")
        return False
    print("Ultralytics installed successfully!")
    return True

def find_dataset():
    """Find the Roboflow dataset"""
    current_dir = Path('.')
    
    # Check for data.yaml in current directory first
    data_yaml = current_dir / 'data.yaml'
    if data_yaml.exists():
        print(f"Found dataset config: {data_yaml}")
        return str(data_yaml)
    
    # Look for dataset directories
    dataset_dirs = [d for d in current_dir.iterdir() if d.is_dir() and 'Fruit' in d.name]
    
    if not dataset_dirs:
        print("No dataset directory found!")
        return None
    
    dataset_dir = dataset_dirs[0]
    data_yaml = dataset_dir / 'data.yaml'
    
    if data_yaml.exists():
        print(f"Found dataset: {dataset_dir}")
        print(f"Data config: {data_yaml}")
        return str(data_yaml)
    else:
        print(f"data.yaml not found in {dataset_dir}")
        return None

def train_yolo_model(data_yaml, model_size='yolo11s-pose.pt'):
    """Train YOLO model"""
    print(f"Training YOLO model with {model_size}...")
    
    try:
        from ultralytics import YOLO
        
        # Load model
        model = YOLO(model_size)
        print(f"Loaded model: {model_size}")
        
        # Train model with YOLO11 optimized settings
        results = model.train(
            data=data_yaml,
            epochs=100,
            imgsz=640,
            batch=16,
            device=0,
            project="Task2_ModelTraining/results",
            name="yolo11s_training",
            save=True,
            save_period=10,
            val=True,
            plots=True,
            # YOLO11 specific optimizations
            optimizer='AdamW',
            lr0=0.001,
            weight_decay=0.0005,
            warmup_epochs=3,
            cos_lr=True,
            close_mosaic=10,
            # Advanced augmentation for YOLO11
            hsv_h=0.015,
            hsv_s=0.7,
            hsv_v=0.4,
            degrees=0.0,
            translate=0.1,
            scale=0.5,
            shear=0.0,
            perspective=0.0,
            flipud=0.0,
            fliplr=0.5,
            mosaic=1.0,
            mixup=0.0
        )
        
        print("Training completed successfully!")
        print(f"Results saved to: Task2_ModelTraining/results/yolo11s_training/")
        return True
        
    except Exception as e:
        print(f"Training failed with error: {e}")
        return False

def main():
    """Main training pipeline"""
    print("=== YOLO Model Training for Task 2 ===")
    
    # Install ultralytics
    if not install_ultralytics():
        return False
    
    # Find dataset
    data_yaml = find_dataset()
    if not data_yaml:
        return False
    
    # Train model
    success = train_yolo_model(data_yaml)
    
    if success:
        print("\n=== Training Complete ===")
        print("Model saved to: Task2_ModelTraining/results/yolo_training/weights/best.pt")
        print("Training plots saved to: Task2_ModelTraining/results/yolo_training/")
        return True
    else:
        print("\n=== Training Failed ===")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
