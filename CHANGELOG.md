# Changelog

## [2.1.0] – 2026-05-02

### Docker & replication

- `Dockerfile.gpu` — PyTorch **2.4.1 + CUDA 12.1** runtime + pinned Ultralytics stack (`requirements-docker.txt`).
- `Dockerfile.cpu` — CPU-only smoke image for import / single-image predict checks.
- `docker-compose.yml` — `gpu`, `gpu-train`, `gpu-track`, `cpu-smoke` services; host bind-mount for `runs/` and outputs.
- `Makefile` — convenience targets (`docker-shell-gpu`, `docker-train-sm`, …).
- `docs/TRAINING_STAGES.md` — numbered pipeline from environment to inference.
- `docs/DOCKER.md` — build/run recipes and GPU troubleshooting.
- `data/external_videos/README.md` — where to drop input MP4s for compose tracking.

## [2.0.0] – 2026-05-02

### Additions (tracked video samples)

- `results/tracked_videos/` — example MP4s with pose/tracking overlays (~8 s full-res + 720p preview), sourced from lab `annotated_videos_30sec`.

### Repository restructure

- Single top-level layout: `weights/`, `scripts/`, `dataset/`, `data/samples/`, `results/`, `configs/`, `docs/`, `examples/`.
- **Weights**: production YOLO11m-Pose checkpoint included as `weights/fruitfly_pose_yolo11m.pt` (~41 MB).
- **Results**: bundled training curves, confusion matrices (PNGs), and `results/training_metrics.csv` (200 epochs).
- **Samples**: one full run-231127 frame CSV under `data/samples/` plus a curvature-corrected excerpt (due to GitHub 100 MB file limit).
- **Documentation**: step-by-step setup, training, inference, and explanation of large binary tracking dumps.
- **Inference**: default model path resolves to repo-root `weights/`.
- **License**: MIT.

Notes: Multi-gigabyte combined tracking CSV and all 48 per-clip curvature files remain **outside** Git (GitHub rejects files over 100 MB). Sharing options are documented in `docs/06_large_tracking_assets.md`.
