# Training workflow

Recommended entry (**`scripts/train_scaled_model.py`** is a symlink to **`pipeline/stages/stage_03_training/train_scaled_model.py`**; use either path):

```
python scripts/train_scaled_model.py \
  --dataset /path/with/data.yaml \
  --project runs/train \
  --epochs 200 \
  --imgsz 2448 \
  --batch 4
```

Key ideas:

1. Matching **effective training magnification** prevents subtle scale-shift between metrics and deployments.
2. Patience defaults align with plateau behavior observed historically (consult `results/training_metrics.csv`).
3. Lower `--imgsz` or `--batch` if GPU VRAM constrained.

Ordered pipeline table: [**`TRAINING_STAGES.md`**](TRAINING_STAGES.md). Reproducible GPU training via Docker: [**`DOCKER.md`**](DOCKER.md) (`gpu-train`).
