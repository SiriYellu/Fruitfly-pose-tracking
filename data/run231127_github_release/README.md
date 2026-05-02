# Run **231127** — curvature-corrected tracking (XZ archives for GitHub)

The original lab exports `tracks_corrected_clip00…47.csv` and **`tracks_corrected_dual_vial.csv` (~13 GB)** exceed **GitHub’s 100 MiB per-file limit**. This directory contains the **same data** in XZ-compressed form that fits that limit.

On the remote repository those `.xz` bytes are delivered through **Git LFS**. After `git clone`, run **`git lfs install`** once and **`git lfs pull`** in the repo root if the `.xz` files look like tiny text stubs instead of archives.

## What is here

| Path | Description |
|------|-------------|
| **`per_clip/Tracks_corrected_img0000.csv.xz` … `img0047.csv.xz`** (48 files) | One file per 30 min vial video (run **231127**). The `imgXXXX` token matches the `video_name` field in the CSV (e.g. `FVI_20231127_151027_img0007`). |
| **`dual_vial/Tracks_corr_dual_vial.part01.csv.xz` … `part39.csv.xz`** (39 files) | Pieces of the merged **dual-vial** curvature-corrected table. **Part 01** begins with the CSV header; **parts 02–39** are continuation rows only so a simple `cat … \| xzcat` reproduces one valid CSV. |
| **`HASHES.sha256`** | Checksums for every `.xz` file (87 lines). |

**Column definitions** are unchanged from the curvature-corrected schema (header row lists all fields).

### Decompress one video (example: img0007)

```bash
xz -dk per_clip/Tracks_corrected_img0007.csv.xz
# produces Tracks_corrected_img0007.csv
```

### Rebuild `tracks_corrected_dual_vial.csv`

```bash
cat $(ls -v dual_vial/Tracks_corr_dual_vial.part*.csv.xz) | xzcat > tracks_corrected_dual_vial.csv
```

Verification: `wc -l` should report **45 879 875** lines (including header).

### Regenerate this folder from your local `final_reportings/`

```bash
scripts/package_run231127_github_release.sh
```

(Edit `SRC_CLIP_DIR` / `SRC_DUAL` in the script if your paths differ.)

## Size note (~6.3 GB `.xz` committed)

Cloning this repository now downloads a **large** packed dataset. Prefer **partial clone** (`--filter=blob:none`) or **sparse checkout** if you only need code and weights.
