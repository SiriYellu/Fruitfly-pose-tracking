## Tracked / pose-visualization samples (after running the model)

These clips show detections **after** inference with the YOLO pose model (bounding boxes / keypoints / IDs as produced in your labeling pipeline—not raw camera-only footage).

| File | Description |
|------|--------------|
| `sample_pose_bytetrack_8s.mp4` | Full-resolution sample (~8 s, ~32 MB): vials with overlays from your trained pose + tracking stack. |
| `sample_pose_bytetrack_preview_720p.mp4` | Lightweight H.264 preview (~720 px height, no audio) for quick viewing or embedding in decks. |

**Source on lab disk:** copied from  
`Traingagain/05_Annotations/annotated_videos_30sec/annotated_video_01.mp4`.

Regenerate variants from any new `.mp4` with:

```bash
python scripts/track_video.py --video your_clip.mp4 --output out_dir/
```
(Same code: `pipeline/stages/stage_04_inference_tracking/track_video.py`.)

For an annotated video export, use Ultralytics’ built-ins, e.g. `YOLO(...).predict(source=..., save=True)` or enable save in tracking per [Ultralytics tracking docs](https://docs.ultralytics.com/modes/track/).
