# Changelog

## [2.4.1] – 2026-05-03

### Sample videos match Task3 multi-track colors

- Regenerated **`sample_pose_bytetrack_8s.mp4`**, **`sample_pose_bytetrack_preview_720p.mp4`**, and **`tracked_videos/sample_batch/*.mp4`** as short **H.264** trims from **`Traingagain/Task3_FlyTracking/03_Results/batch_videos/tracked_video_*.mp4`**, preserving **2448×2048** full-res visuals and **`track_id`-indexed** bbox/label colors (vs. older annotation exports that drew all-green boxes).
- Updated **`tracked_videos/README.md`**, **`sample_batch/README.md`**, and root **`README.md`** provenance/size notes.

## [2.4.0] – 2026-05-02

### Extra batch demo videos

- **`pipeline/stages/stage_05_evaluation_reports/results/tracked_videos/sample_batch/`** — three extra **~8 s** QA clips alongside the primary demo; **v2.4.1** re-sourced them from Task3 **colored** batch exports—see **`tracked_videos/README.md`**.

### Repo layout matches pipeline stages

- **`dataset/`**, **`configs/`**, and **`weights/`** → **`pipeline/stages/stage_02_dataset_config_weights/`**
- **`results/`** (metrics, curves, sample MP4s) → **`pipeline/stages/stage_05_evaluation_reports/results/`**
- **`examples/load_and_infer.py`** → **`pipeline/stages/stage_04_inference_tracking/load_and_infer.py`** (root **`examples/README.md`** points here)
- Training / tracking **defaults** and **`configs/tracking.yaml`** now reference repo-root paths under **`pipeline/stages/stage_02_dataset_config_weights/`**. Docker Compose, **`Dockerfile.cpu`**, and docs updated accordingly.

## [2.3.0] – 2026-05-02

### Pipeline stages (canonical code paths)

- New **`pipeline/stages/`** tree: **`stage_01_environment`** … **`stage_06_publish_release`** (`README.md` per stage plus executable files in train / inference / publish stages).
- **`train_scaled_model.py`**, **`track_video.py`**, and **`package_run231127_github_release.sh`** live under **`pipeline/stages/`**; repo-root **`scripts/`** holds **symlinks** so Docker Compose and existing CLI examples keep working.
- **`pipeline/README.md`**, **`scripts/README.md`**, and rewritten **`docs/TRAINING_STAGES.md`** document Stage **01–06** and map to **`docs/`** narratives.

## [2.2.0] – 2026-05-02

### Published curvature-corrected tracking bundle (XZ)

- `data/run231127_github_release/` — **48** per-video curvature-corrected tracks (`Tracks_corrected_img0000.csv.xz` … `img0047.csv.xz`).
- **`tracks_corrected_dual_vial.csv`**-equivalent shipped as **39** XZ chunks (`dual_vial/Tracks_corr_dual_vial.part*.csv.xz`); concatenate with sorted `xzcat`.
- `pipeline/stages/stage_06_publish_release/package_run231127_github_release.sh` regenerates this tree from lab `tracks_corrected_clip*` + `tracks_corrected_dual_vial.csv` (shortcut: **`scripts/package_run231127_github_release.sh`** symlink).
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
