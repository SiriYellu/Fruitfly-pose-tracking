# Stage 04 — Inference and multi-object tracking

**Goal:** Run pose + **ByteTrack** on MP4 exports → per-frame CSV.

**Scripts:**

| File | Purpose |
|------|---------|
| [`track_video.py`](track_video.py) | Full-video tracking + CSV (default weights under `weights/`). |
| [`../../../examples/load_and_infer.py`](../../../examples/load_and_infer.py) | One-image **`predict`** smoke (used by Compose `cpu-smoke`). |

**Example:**

```bash
python pipeline/stages/stage_04_inference_tracking/track_video.py \
  --video path/to/vial_clip.mp4 --output outputs/run1/
```

Equivalent: `python scripts/track_video.py …`

**Next:** [`../stage_05_evaluation_reports/README.md`](../stage_05_evaluation_reports/README.md).

**Docs:** [`docs/04_inference.md`](../../../docs/04_inference.md).
