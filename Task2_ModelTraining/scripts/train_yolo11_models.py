#!/usr/bin/env python3
"""
Train YOLO11s-pose and YOLO11m-pose models for comparison
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

def train_yolo_model(data_yaml, model_size, model_name):
    """Train YOLO model"""
    print(f"\n{'='*60}")
    print(f"Training {model_name} ({model_size})")
    print(f"{'='*60}")
    
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
            name=model_name,
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
        
        print(f"✅ {model_name} training completed successfully!")
        print(f"Results saved to: Task2_ModelTraining/results/{model_name}/")
        return True
        
    except Exception as e:
        print(f"❌ {model_name} training failed with error: {e}")
        return False

def compare_models():
    """Compare the trained models"""
    print(f"\n{'='*60}")
    print("MODEL COMPARISON SUMMARY")
    print(f"{'='*60}")
    
    models = [
        ("YOLO11n-pose", "yolo11_training"),
        ("YOLO11s-pose", "yolo11s_training"), 
        ("YOLO11m-pose", "yolo11m_training"),
        ("YOLOv8s-pose", "yolo_training")
    ]
    
    print(f"{'Model':<20} {'Status':<15} {'Best mAP50':<12} {'Model Size':<12}")
    print("-" * 60)
    
    for model_name, training_dir in models:
        results_dir = Path(f"Task2_ModelTraining/results/{training_dir}")
        best_pt = results_dir / "weights" / "best.pt"
        
        if best_pt.exists():
            size_mb = best_pt.stat().st_size / (1024 * 1024)
            print(f"{model_name:<20} {'✅ Trained':<15} {'Available':<12} {size_mb:.1f}MB")
        else:
            print(f"{model_name:<20} {'❌ Not found':<15} {'N/A':<12} {'N/A':<12}")

def main():
    """Main training pipeline"""
    print("🚀 YOLO11 Model Training Pipeline")
    print("=" * 60)
    
    # Install ultralytics
    if not install_ultralytics():
        return False
    
    # Find dataset
    data_yaml = find_dataset()
    if not data_yaml:
        return False
    
    # Models to train
    models_to_train = [
        ("yolo11s-pose.pt", "yolo11s_training"),
        ("yolo11m-pose.pt", "yolo11m_training")
    ]
    
    success_count = 0
    
    # Train each model
    for model_size, model_name in models_to_train:
        if train_yolo_model(data_yaml, model_size, model_name):
            success_count += 1
        else:
            print(f"❌ Failed to train {model_name}")
    
    # Compare models
    compare_models()
    
    print(f"\n{'='*60}")
    print(f"TRAINING SUMMARY")
    print(f"{'='*60}")
    print(f"Models trained successfully: {success_count}/{len(models_to_train)}")
    
    if success_count > 0:
        print("🎉 Training completed! Check results for model comparison.")
        return True
    else:
        print("❌ All training failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

