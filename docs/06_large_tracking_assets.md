# Hosting large behavioural CSV exports

Artifacts exceeding roughly **90–100 MB** each must **not** be committed verbatim to Git (GitHub rejects >100 MB blobs without LFS quotas).

Historical deliverables exceeding limit:

| Name | Typical size | Notes |
|------|---------------|-------|
| `tracks_corrected_dual_vial.csv` | ~13 GB merged | Population-scale stats |
| Per-clip corrected CSV | ~170–260 MB | 48 clips run 231127 |
| Selected raw pixel dumps | ~80–160 MB | Still borderline singularly |

Recommendation:

1. **Zenodo archive** (+ DOI citation)
2. **Institutional HTTPS / S3-compatible bucket** (+ checksum manifest)
3. Optional **multi-part GitHub Release** only if segmented & <2 GB per segment
