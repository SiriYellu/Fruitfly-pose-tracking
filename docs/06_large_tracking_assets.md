# Hosting large behavioural CSV exports

Artifacts exceeding roughly **90–100 MB** each must **not** be committed verbatim to Git (GitHub rejects blobs > ~100 MB unless using **Git Large File Storage**).

## Included in **this repo** (XZ shards)

Curvature-corrected run **231127** ships under **`data/run231127_github_release/`** as **xz-compressed CSV** shards (each shard < 100 MB): 48 **`Tracks_corrected_imgXXXX.csv.xz`** plus 39 chunk files named **`Tracks_corr_dual_vial.partNN.csv.xz`**. On GitHub those archives are stored with **Git LFS**: run **`git lfs install`** and **`git lfs pull`** after clone to fetch ~**6 GB**. See **`data/run231127_github_release/README.md`** for `xzcat`/concatenate and **`HASHES.sha256`**. Use sparse checkout if you want to skip the **`data/`** tree entirely.

## Raw exports (typically not in repo)

| Name | Typical size | Notes |
|------|---------------|-------|
| `tracks_corrected_dual_vial.csv` | ~13 GB merged | Population-scale stats |
| Per-clip corrected CSV | ~170–260 MB | 48 clips run 231127 |
| Selected raw pixel dumps | ~80–160 MB | Still borderline singularly |

### Other hosting options

1. **Zenodo archive** (+ DOI citation)
2. **Institutional HTTPS / S3-compatible bucket** (+ checksum manifest)
3. Optional **multi-part GitHub Release** only if segmented and < 100 MB each (or Git LFS)
