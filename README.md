# Fruit fly pose estimation and vial tracking

Pose-based detection and multi-fly tracking for *Drosophila* in standard food-vial recordings (approximately **2448×2048**, 30 fps). This repository ships a trained **YOLO11m-Pose** model (**three keypoints**: head, thorax, abdomen), inference scripts (**ByteTrack**), a small reproducible **YOLO dataset** slice, and **exported training metrics / figures**.

> **Large tracking bundle:** run **231127** curvature-corrected exports live under **`data/run231127_github_release/`** as **XZ** shards, stored with **[Git LFS](https://git-lfs.com/)** (~6 GB payload). Install `git-lfs`, run **`git lfs install`** once, then **`git lfs pull`** after clone so the `.xz` files materialize as real archives—not the small pointer stubs Git stores in commits. Plain Git cannot accept a multi-gigabyte single push pack on GitHub, so Git LFS is required for this subtree; see **`data/run231127_github_release/README.md`** and [`docs/06_large_tracking_assets.md`](docs/06_large_tracking_assets.md).

---

## Layout

```
.
├── CHANGELOG.md
├── README.md                   # ← you are here
├── LICENSE                     # MIT
├── requirements.txt
├── configs/
│   └── tracking.yaml           # Inference / geometry defaults (reference)
├── weights/
│   ├── README.md
│   └── fruitfly_pose_yolo11m.pt   # Production checkpoint (~41 MB)
├── scripts/
│   ├── track_video.py          # Pose + ByteTrack → per-frame CSV
│   └── train_scaled_model.py   # Full-resolution training starter
├── dataset/
│   └── yolo_pose/              # Minimal YOLO pose split + data.yaml (Roboflow lineage)
├── data/
│   ├── README.md
│   ├── run231127_github_release/   # 48 per-video + 39 dual-vial shard XZ (~6 GB tracked)
│   ├── roboflow/roboflow_export_yolov8_pose.zip
│   └── samples/
├── results/
│   ├── training_metrics.csv    # Epoch-by-epoch log (validation)
│   ├── training_curves/        # Publication-style PNG curves
│   ├── confusion_matrices/
│   └── tracked_videos/         # Sample MP4s with pose/track overlays after inference
├── docs/                       # Step-by-step narratives + Docker + pipeline stages
├── docker-compose.yml
├── Dockerfile.gpu
├── Dockerfile.cpu
├── Makefile                    # shortcut: make docker-shell-gpu, etc.
├── examples/
│   └── load_and_infer.py
```

See [`CHANGELOG.md`](CHANGELOG.md) for v2 restructuring notes.

---

## Sample videos (model applied)

Qualitative demos with **detections / keypoints / track IDs overlaid**:

| Clip | Location |
|------|-----------|
| ~8 s, full-res (~32 MB) | [`results/tracked_videos/sample_pose_bytetrack_8s.mp4`](results/tracked_videos/sample_pose_bytetrack_8s.mp4) |
| ~8 s, 720p preview (~1 MB) | [`results/tracked_videos/sample_pose_bytetrack_preview_720p.mp4`](results/tracked_videos/sample_pose_bytetrack_preview_720p.mp4) |

See [`results/tracked_videos/README.md`](results/tracked_videos/README.md) for provenance.

---

## Quick start — inference

```bash
python -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126   # adapt to your CUDA
pip install -r requirements.txt

# From repo root (GPU):
python scripts/track_video.py \
  --video /path/to/vial_clip.mp4 \
  --output outputs/run_a/ \
  --device cuda:0
```

Produces `*_tracking.csv` with columns for frame index, ByteTrack IDs, bbox, normalized confidences, and keypoint XY + visibility bits.

Detailed flags and Ultralytics quirks: [`docs/04_inference.md`](docs/04_inference.md).

---

## Training / fine-tuning

The production checkpoint was optimized on a **resolution-matched** (scaled/full-frame) annotated corpus. Bundled **`dataset/yolo_pose/`** is a **minimal** pedagogical subset (demo + sanity checks)—scale up privately with your expanded frames before expecting production-level metrics.

```bash
python scripts/train_scaled_model.py \
  --dataset /your/scaled_dataset \
  --project runs/train \
  --epochs 200 --imgsz 2448 --batch 4
```

More context: [`docs/03_training.md`](docs/03_training.md).

---

## Results bundled in-repo

| Item | Location |
|------|-----------|
| Per-epoch validation metrics CSV | [`results/training_metrics.csv`](results/training_metrics.csv) |
| Training curve PNG set | [`results/training_curves/`](results/training_curves/) |
| Confusion-matrix PNG set | [`results/confusion_matrices/`](results/confusion_matrices/) |
| Human-readable metric summary | [`docs/05_training_and_metrics.md`](docs/05_training_and_metrics.md) |

Approximate headline numbers at **epoch 200** (see CSV): pose **mAP50 ≈ 0.985**, pose **mAP50–95 ≈ 0.975**.

---

## Sample tracking CSVs (`data/samples/`)

See [`data/README.md`](data/README.md). Shipped artifacts:

1. **`frame_by_frame/`** — one complete *run 231127* clip (pixels, track IDs).
2. **`curvature_corrected/`** — first **50,000** rows of `tracks_corrected_clip15.csv` illustrating millimeter curvature-corrected schema.

Full 48 × 30 min exports + merged >10 GB corpus: [`docs/06_large_tracking_assets.md`](docs/06_large_tracking_assets.md).

---

## Reproducibility — training stages & Docker

| Resource | Purpose |
|----------|---------|
| [`docs/TRAINING_STAGES.md`](docs/TRAINING_STAGES.md) | Numbered pipeline: environment → dataset → train → weights → track |
| [`docs/DOCKER.md`](docs/DOCKER.md) | GPU/CPU images, Compose services, troubleshooting |
| `Dockerfile.gpu` / `Dockerfile.cpu` | Pinned PyTorch CUDA base + Ultralytics deps |
| `requirements-docker.txt` | Version-pinned installs **on top** of the GPU base image |
| `docker-compose.yml` | `gpu`, `gpu-train`, `gpu-track`, `cpu-smoke` services |
| `Makefile` | `make docker-shell-gpu`, `make docker-train-sm`, etc.

Quick GPU shell:

```bash
docker compose build gpu
docker compose run --rm --gpus all gpu bash
```

---

## Documentation index

| Doc | Topics |
|-----|--------|
| [`docs/00_overview.md`](docs/00_overview.md) | End-to-end pipeline narrative |
| [`docs/01_setup.md`](docs/01_setup.md) | Python, CUDA, common install failures |
| [`docs/02_data.md`](docs/02_data.md) | Annotations, keypoint order, Roboflow |
| [`docs/03_training.md`](docs/03_training.md) | Resolution scaling, epochs, GPUs |
| [`docs/TRAINING_STAGES.md`](docs/TRAINING_STAGES.md) | Stage table — easiest replication roadmap |
| [`docs/04_inference.md`](docs/04_inference.md) | Confidence, trackers, throughput |
| [`docs/05_training_and_metrics.md`](docs/05_training_and_metrics.md) | Parsing `training_metrics.csv` |
| [`docs/06_large_tracking_assets.md`](docs/06_large_tracking_assets.md) | Multi-GB bundles & hosting playbook |
| [`docs/DOCKER.md`](docs/DOCKER.md) | Docker + Compose recipes |

---

## Citation

If you use this codebase or checkpoints in research, please cite the GitHub repository and (when published) the associated paper—you can adapt:

```bibtex
@misc{fruitfly_pose_tracking_repo,
  title        = {Fruit Fly Pose Tracking},
  author       = {Yellu, Siri},
  year         = {2026},
  howpublished = {\url{https://github.com/SiriYellu/Fruitfly-pose-tracking}},
  note         = {YOLO11m pose + ByteTrack inference; training metrics \& weights}
}
```

---

## Contributing / issues

Open GitHub Issues for reproducibility gaps (paths, Ultralytics warnings, CUDA wheels). Prefer **minimal** reproducible snippets when reporting bugs.

---

**Maintainer**: [SiriYellu](https://github.com/SiriYellu) · Repo: [`Fruitfly-pose-tracking`](https://github.com/SiriYellu/Fruitfly-pose-tracking)
