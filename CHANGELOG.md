# Changelog

## [2.2.0] – 2026-05-02

### Published curvature-corrected tracking bundle (XZ)

- `data/run231127_github_release/` — **48** per-video curvature-corrected tracks (`Tracks_corrected_img0000.csv.xz` … `img0047.csv.xz`).
- **`tracks_corrected_dual_vial.csv`**-equivalent shipped as **39** XZ chunks (`dual_vial/Tracks_corr_dual_vial.part*.csv.xz`); concatenate with sorted `xzcat`.
- `scripts/package_run231127_github_release.sh` regenerates this tree from lab `tracks_corrected_clip*` + `tracks_corrected_dual_vial.csv`.
- `docs/06_large_tracking_assets.md` — GitHub/Zenodo note for blobs > 100 MB.

GitHub forbids blobs > ~100 MB; uncompressed dual-vial CSV (~13 GB) and per-clip CSVs (**~170–350 MB**) are archived as `.xz`; see `data/run231127_github_release/README.md` for decompression and checksums.

**Git LFS:** the `.xz` archives are stored with **Git Large File Storage** (small pointers in commits; blobs upload via `git push`). Install [Git LFS](https://git-lfs.com/) (`git lfs install`) before clone/push/pull of this repo. A plain-Git-only push exceeds GitHub's **pack unpack** limit (~2 GiB), so **87** binaries use LFS.

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
