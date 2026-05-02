#!/usr/bin/env python3
"""Minimal Ultralytics inference example using repo weights (stage 04)."""

from pathlib import Path

from ultralytics import YOLO

REPO_ROOT = Path(__file__).resolve().parents[3]
STAGE_02 = REPO_ROOT / "pipeline" / "stages" / "stage_02_dataset_config_weights"
WEIGHTS = STAGE_02 / "weights" / "fruitfly_pose_yolo11m.pt"


def main():
    model = YOLO(str(WEIGHTS))
    # Replace with your image or video path
    sample = STAGE_02 / "dataset" / "yolo_pose" / "train" / "images"
    imgs = sorted(sample.glob("*.jpg"))[:1]
    if not imgs:
        print(f"No demo images under {sample}")
        return
    results = model.predict(source=str(imgs[0]), conf=0.28, save=False)
    r = results[0]
    print("boxes:", len(r.boxes) if r.boxes is not None else 0)


if __name__ == "__main__":
    main()
