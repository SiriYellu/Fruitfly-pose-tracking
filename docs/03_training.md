# Training workflow

Recommended entry (`repo` root assumed):

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
