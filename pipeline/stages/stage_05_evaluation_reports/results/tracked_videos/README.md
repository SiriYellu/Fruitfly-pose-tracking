## Tracked / pose-visualization samples (after running the model)

These clips show detections **after** inference with the YOLO pose model **plus ByteTrack**. Bounding boxes and `T{id}` labels use a **per-track color cycle** (see `batch_tracking_generator.py` in `Traingagain/Task3_FlyTracking`), not uniform green—which matches what you see in full batch exports.

| File | Description |
|------|--------------|
| `sample_pose_bytetrack_8s.mp4` | Full-resolution **H.264** sample (~8 s, **2448×2048**, ~2–3 MB in repo): trimmed from Task3 **`tracked_video_1.mp4`**. |
| `sample_pose_bytetrack_preview_720p.mp4` | First ~8 s scaled to ~720 px height, H.264, no audio, for decks / compose defaults. |

**Extra vials for batch QA:** [`sample_batch/`](sample_batch/) — three more **~8 s** trims from **`tracked_video_2` … `tracked_video_4`**; same visualization code path.

**Lab sources (canonical):**

- Primary trim:  
  `Traingagain/Task3_FlyTracking/03_Results/batch_videos/batch_output_20250929_221529/tracked_video_1.mp4`
- Batch folder:  
  `Traingagain/Task3_FlyTracking/03_Results/batch_videos/`

Full-length **README demos** (**~60 s × 5**, H.264, per-track colors) live in **`batch_full/`** with GIF/poster previews; originals also remain on disk under `Traingagain/.../batch_videos/` if needed.
**Rebuild similar overlays:** colored MP4s like these are emitted by **`Traingagain/Task3_FlyTracking`** batch scripts (see **`batch_tracking_generator.py`** → `tracked_video_*.mp4`). Repo clips are FFmpeg **H.264** trims (`-ss 0 -t 8`, `libx264`) of those exports.

Tracks to CSV **without drawing** on frames:

```bash
python scripts/track_video.py --video your_clip.mp4 --output out_dir/
```
(Same code: `pipeline/stages/stage_04_inference_tracking/track_video.py`; use Ultralytics **`save=True`** tracking if you want built-in plotted video from weights in-repo.)
