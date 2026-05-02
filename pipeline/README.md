# Pipeline overview (numbered stages)

Run stages in order for a full reproducible path **from environment to published tracking bundles**. Shortcut: use **`pipeline/stages/stage_02_dataset_config_weights/weights/fruitfly_pose_yolo11m.pt`** and jump to **stage 04** for inference-only work.

| Stage | Directory | Goal |
|------|-----------|------|
| **01** Environment | [`stages/stage_01_environment/`](stages/stage_01_environment/README.md) | Python/CUDA deps, **`requirements*.txt`**, **`Dockerfile.*`**, **`docker-compose.yml`**. |
| **02** Dataset · config · weights | [`stages/stage_02_dataset_config_weights/`](stages/stage_02_dataset_config_weights/README.md) | **`dataset/yolo_pose/`**, **`configs/tracking.yaml`**, **`weights/`** (production checkpoint). |
| **03** Training | [`stages/stage_03_training/`](stages/stage_03_training/README.md) | Fine-tune YOLO11m-Pose: **`train_scaled_model.py`**. |
| **04** Inference / tracking | [`stages/stage_04_inference_tracking/`](stages/stage_04_inference_tracking/README.md) | Pose + ByteTrack CSV: **`track_video.py`**; **`load_and_infer.py`** (minimal predict smoke). |
| **05** Evaluation & reports | [`stages/stage_05_evaluation_reports/`](stages/stage_05_evaluation_reports/README.md) | **`results/`** metrics, curves, **`docs/05_training_and_metrics.md`**. |
| **06** Publish / release data | [`stages/stage_06_publish_release/`](stages/stage_06_publish_release/README.md) | Compress & shard curvature-corrected CSVs for GitHub LFS (**`package_run231127_github_release.sh`**). |

## Back-compat entry points (`scripts/`)

For historical commands and Compose, **`scripts/`** holds **symlinks** to the canonical files under **`pipeline/stages/`** (Unix-friendly; enable symlink support if you clone on Windows).
