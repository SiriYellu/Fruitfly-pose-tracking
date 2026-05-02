# Stage 06 — Publish / release tracking data

**Goal:** Produce **xz-compressed** per-clip and dual-vial shards (< 100 MB each) suitable for **Git + Git LFS**, plus `HASHES.sha256`.

**Script:** [`package_run231127_github_release.sh`](package_run231127_github_release.sh)

Uses lab-side sources via `SRC_CLIP_DIR` / `SRC_DUAL` (defaults under `final_reportings/` — adjust on your disk). Writes to `data/run231127_github_release/`.

Equivalent (symlink): `scripts/package_run231127_github_release.sh`

**Docs:** [`data/run231127_github_release/README.md`](../../../data/run231127_github_release/README.md), [`docs/06_large_tracking_assets.md`](../../../docs/06_large_tracking_assets.md).
