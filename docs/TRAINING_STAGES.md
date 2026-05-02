# Training pipeline — stages (reproduce in order)

Each stage has a **goal**, **inputs**, and **outputs**. You can stop after any stage if you only need inference with the shipped `weights/fruitfly_pose_yolo11m.pt`.

| Stage | Goal | Where in repo |
|-------|------|----------------|
| **0** | Reproducible environment (venv or Docker) | [`01_setup.md`](01_setup.md), [`DOCKER.md`](DOCKER.md), `Dockerfile.gpu` |
| **1** | YOLO-pose layout + valid `data.yaml` | [`02_data.md`](02_data.md), [`dataset/`](../dataset/) |
| **2** | (Automatic) Ultralytics fetches `yolo11m-pose.pt` on first training run | — |
| **3** | Train / fine-tune (`imgsz`, `batch`, `epochs`) | [`03_training.md`](03_training.md), [`scripts/train_scaled_model.py`](../scripts/train_scaled_model.py) |
| **4** | Checkpoints under `runs/train/<run>/weights/` | Not committed |
| **5** | Inference + ByteTrack → CSV | [`04_inference.md`](04_inference.md), [`scripts/track_video.py`](../scripts/track_video.py) |

## Historical production-scale settings

The shipped `results/training_metrics.csv` comes from training at **effective full vial resolution** (~2448), **YOLO11m-Pose**, long schedules (~**200 epochs**), tuned for workstation GPUs.

**Docker defaults** deliberately use smaller `imgsz` / `epochs` first so newcomers can validate the stack; ramp with environment variables documented in [`DOCKER.md`](DOCKER.md).

## Host commands (non-Docker)

```bash
python scripts/train_scaled_model.py \
  --dataset dataset/yolo_pose \
  --project runs/train \
  --epochs 200 --imgsz 2448 --batch 4

python scripts/track_video.py --video clip.mp4 --output outputs/run1/
```

## Docker equivalents

[`DOCKER.md`](DOCKER.md) lists `docker compose run --gpus all ...` recipes and [`Makefile`](../Makefile) shortcuts.
