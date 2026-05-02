# Inference CLI

Canonical script: `scripts/track_video.py`.

Core invocation:

```
python scripts/track_video.py \
  --video VIDEO.mp4 \
  --output OUT_DIR/
```

Important flags:

| Flag | Default | Notes |
|------|---------|-------|
| `--model` | `weights/fruitfly_pose_yolo11m.pt` | Alternate fine-tuned weights OK |
| `--conf` | 0.28 | Confidence |
| `--iou` | 0.7 | NMS IoU overlap |
| `--device` | `cuda:0` | Fallback `cpu` possible |
| `--batch` | off | Recursive directory ingest `*.mp4` |
