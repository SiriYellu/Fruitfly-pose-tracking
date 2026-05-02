#!/usr/bin/env python3
"""
Train YOLO11m-Pose on a YOLO-format dataset at native vial resolution (default imgsz 2448).
This mirrors the scalable training recipe used for the production checkpoint — adjust paths
for your scaled/full-resolution dataset (see docs/03_training.md).

Canonical path (pipeline stage 03):
  python pipeline/stages/stage_03_training/train_scaled_model.py \\
    --dataset dataset/yolo_pose --project runs/train

Back-compat symlink:
  python scripts/train_scaled_model.py --dataset dataset/yolo_pose --project runs/train
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import torch
from ultralytics import YOLO

REPO_ROOT = Path(__file__).resolve().parents[3]


def train_scaled(dataset_dir: Path, project: Path, run_name: str | None = None, epochs: int = 200, imgsz: int = 2448, batch: int = 4) -> Path:
    dataset_dir = Path(dataset_dir).resolve()
    project = Path(project).resolve()
    project.mkdir(parents=True, exist_ok=True)
    rid = run_name or f"scaled_pose_{os.getenv('SLURM_JOB_ID', 'local')}_{os.getpid()}"

    data_yaml = dataset_dir / "data.yaml"
    if not data_yaml.exists():
        raise FileNotFoundError(f"Missing {data_yaml}")

    print(f"Dataset: {dataset_dir}")
    print(f"Project: {project} / {rid}")

    model = YOLO("yolo11m-pose.pt")

    kw = dict(
        data=str(data_yaml),
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        device="cuda" if torch.cuda.is_available() else "cpu",
        workers=4,
        patience=50,
        save_period=25,
        cache=False,
        project=str(project),
        name=rid,
        exist_ok=True,
        val=True,
        box=0.2,
        cls=0.3,
        dfl=6.0,
        hsv_h=0.01,
        hsv_s=0.5,
        hsv_v=0.3,
        degrees=10.0,
        translate=0.05,
        scale=0.3,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=0.5,
        mixup=0.0,
        copy_paste=0.0,
        optimizer="AdamW",
        lr0=0.001,
        lrf=0.0001,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=20,
        warmup_momentum=0.8,
        warmup_bias_lr=0.1,
        cos_lr=True,
        close_mosaic=20,
        amp=True,
    )

    model.train(**kw)
    metrics = model.val(data=str(data_yaml), imgsz=imgsz, batch=max(2, batch // 2), conf=0.001, iou=0.7, project=str(project), name=rid, exist_ok=True)
    print(f"Pose mAP50={metrics.pose.map50:.4f}  Pose mAP50-95={metrics.pose.map:.4f}")
    return project / rid


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", type=Path, default=REPO_ROOT / "dataset" / "yolo_pose", help="Folder containing data.yaml train/ valid/ test/")
    p.add_argument("--project", type=Path, default=REPO_ROOT / "runs" / "train", help="Ultralytics project dir")
    p.add_argument("--name", default=None)
    p.add_argument("--epochs", type=int, default=200)
    p.add_argument("--imgsz", type=int, default=2448)
    p.add_argument("--batch", type=int, default=4)
    args = p.parse_args()
    train_scaled(args.dataset, args.project, args.name, args.epochs, args.imgsz, args.batch)


if __name__ == "__main__":
    main()
