# Stage 03 — Training

**Goal:** Train or fine-tune **YOLO11m-Pose** at vial-aligned resolution (`imgsz`, `batch`, `epochs` configurable).

**Script:** [`train_scaled_model.py`](train_scaled_model.py)

**Example (repo root):**

```bash
python pipeline/stages/stage_03_training/train_scaled_model.py \
  --dataset pipeline/stages/stage_02_dataset_config_weights/dataset/yolo_pose --project runs/train --epochs 10 --imgsz 640 --batch 2
```

Equivalent (symlink): `python scripts/train_scaled_model.py …`

Ultralytics writes checkpoints under `runs/train/<run>/weights/` (**not committed**).

**Next:** [`../stage_04_inference_tracking/README.md`](../stage_04_inference_tracking/README.md).

**Docs:** [`docs/03_training.md`](../../../docs/03_training.md).
