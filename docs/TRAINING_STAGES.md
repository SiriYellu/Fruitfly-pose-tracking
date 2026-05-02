# Training pipeline — stages (reproduce in order)

The repo organizes work as **six numbered stages** under [`pipeline/`](../pipeline/) (see **[`pipeline/README.md`](../pipeline/README.md)**). These map to narrative docs below.

You can stop after any stage; for inference-only work, skip to **stage 04** once **`pipeline/stages/stage_02_dataset_config_weights/weights/fruitfly_pose_yolo11m.pt`** exists.

## Stage ↔ repo map

| Stage | Goal | Code / location | Docs |
|-------|------|-----------------|------|
| **01** | Environment (venv or Docker) | `requirements*.txt`, `Dockerfile.*`, `docker-compose.yml` | [`01_setup.md`](01_setup.md), [`DOCKER.md`](DOCKER.md) |
| **02** | YOLO-pose layout, `data.yaml`, weights · config | [`pipeline/stages/stage_02_dataset_config_weights/`](../pipeline/stages/stage_02_dataset_config_weights/README.md) | [`02_data.md`](02_data.md) |
| **03** | Train / fine-tune (`imgsz`, `batch`, `epochs`) | [`pipeline/stages/stage_03_training/train_scaled_model.py`](../pipeline/stages/stage_03_training/train_scaled_model.py) (same as **`scripts/train_scaled_model.py`** symlink) | [`03_training.md`](03_training.md) |
| *(auto)* | Ultralytics fetches **`yolo11m-pose.pt`** on first training run | — | — |
| **04** | Inference + ByteTrack → CSV | [`pipeline/stages/stage_04_inference_tracking/track_video.py`](../pipeline/stages/stage_04_inference_tracking/track_video.py) (=`scripts/track_video.py`) | [`04_inference.md`](04_inference.md) |
| **05** | Bundled training metrics, curves, sample overlays | [`pipeline/stages/stage_05_evaluation_reports/results/`](../pipeline/stages/stage_05_evaluation_reports/results/README.md) (+ Ultralytics checkpoints under **`runs/train/<run>/weights/`** when you train locally) | [`05_training_and_metrics.md`](05_training_and_metrics.md) |
| **06** | Publish large curvature CSVs as XZ shards (optional) | [`pipeline/stages/stage_06_publish_release/package_run231127_github_release.sh`](../pipeline/stages/stage_06_publish_release/package_run231127_github_release.sh) | [`06_large_tracking_assets.md`](06_large_tracking_assets.md) |

## Historical production-scale settings

The shipped **`pipeline/stages/stage_05_evaluation_reports/results/training_metrics.csv`** comes from training at **effective full vial resolution** (~2448), **YOLO11m-Pose**, long schedules (~**200 epochs**), tuned for workstation GPUs.

**Docker defaults** deliberately use smaller `imgsz` / `epochs` first so newcomers can validate the stack; ramp with environment variables documented in [`DOCKER.md`](DOCKER.md).

## Host commands (non-Docker)

```bash
python pipeline/stages/stage_03_training/train_scaled_model.py \
  --dataset pipeline/stages/stage_02_dataset_config_weights/dataset/yolo_pose \
  --project runs/train \
  --epochs 200 --imgsz 2448 --batch 4

python pipeline/stages/stage_04_inference_tracking/track_video.py \
  --video clip.mp4 --output outputs/run1/
```

## Docker equivalents

[`DOCKER.md`](DOCKER.md) lists `docker compose run --gpus all …` recipes and [`Makefile`](../Makefile) shortcuts. Compose commands still invoke **`scripts/…`** (symlinks) for stable paths inside the container.
