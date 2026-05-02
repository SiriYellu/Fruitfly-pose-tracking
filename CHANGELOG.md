# Changelog

## [2.0.0] – 2026-05-02

### Repository restructure

- Single top-level layout: `weights/`, `scripts/`, `dataset/`, `data/samples/`, `results/`, `configs/`, `docs/`, `examples/`.
- **Weights**: production YOLO11m-Pose checkpoint included as `weights/fruitfly_pose_yolo11m.pt` (~41 MB).
- **Results**: bundled training curves, confusion matrices (PNGs), and `results/training_metrics.csv` (200 epochs).
- **Samples**: one full run-231127 frame CSV under `data/samples/` plus a curvature-corrected excerpt (due to GitHub 100 MB file limit).
- **Documentation**: step-by-step setup, training, inference, and explanation of large binary tracking dumps.
- **Inference**: default model path resolves to repo-root `weights/`.
- **License**: MIT.

Notes: Multi-gigabyte combined tracking CSV and all 48 per-clip curvature files remain **outside** Git (GitHub rejects files over 100 MB). Sharing options are documented in `docs/06_large_tracking_assets.md`.
