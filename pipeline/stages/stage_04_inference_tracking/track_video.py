#!/usr/bin/env python3
"""
Track fruit flies in vial videos with YOLO11m-Pose + ByteTrack.
Default model path resolves to weights/fruitfly_pose_yolo11m.pt at repo root.

Canonical path (pipeline stage 04):
  python pipeline/stages/stage_04_inference_tracking/track_video.py \\
    --video path/to/video.mp4 --output outputs/run1/

Back-compat symlink:
  python scripts/track_video.py --video path/to/video.mp4 --output outputs/run1/
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

try:
    from ultralytics import YOLO
except ImportError:
    print("ERROR: install ultralytics: pip install -r requirements.txt")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODEL = REPO_ROOT / "weights" / "fruitfly_pose_yolo11m.pt"


class FlyTracker:
    """YOLO pose estimation + ByteTrack multi-object tracking."""

    def __init__(
        self,
        model_path: Path,
        conf_threshold: float = 0.28,
        iou_threshold: float = 0.7,
        device: str = "cuda:0",
    ):
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        self.model = YOLO(str(self.model_path))
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.device = device

    def process_video(
        self,
        video_path: Path,
        output_dir: Path,
        save_csv: bool = True,
        save_video: bool = False,
    ) -> Path | None:
        video_path = Path(video_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        if not video_path.exists():
            raise FileNotFoundError(video_path)

        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        print(f"{video_path.name}: {width}x{height}, {fps} FPS, ~{total_frames} frames")

        results = self.model.track(
            source=str(video_path),
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            persist=True,
            tracker="bytetrack.yaml",
            stream=True,
            device=self.device,
            verbose=False,
        )

        rows: list[dict] = []
        frame_idx = 0
        if save_video:
            print("Note: annotated video export use model.predict(..., save=True) — see docs/04_inference.md")

        for result in results:
            frame_idx += 1
            if getattr(result, "boxes", None) is None or len(result.boxes) == 0:
                continue

            boxes = result.boxes.xyxy.cpu().numpy()
            track_ids = result.boxes.id
            if track_ids is not None:
                track_ids = track_ids.cpu().numpy().astype(int)
            else:
                track_ids = np.full(len(boxes), -1, dtype=int)
            confidences = result.boxes.conf.cpu().numpy()

            kxy = kv = None
            if getattr(result, "keypoints", None) is not None and len(result.keypoints) > 0:
                kxy = result.keypoints.xy.cpu().numpy()
                kv = result.keypoints.visible.cpu().numpy()

            for i, (box, track_id, conf) in enumerate(zip(boxes, track_ids, confidences)):
                x1, y1, x2, y2 = box
                cx = float((x1 + x2) / 2)
                cy = float((y1 + y2) / 2)

                hx = hy = hv = tx = ty = tv = ax = ay = av = None
                if kxy is not None and i < len(kxy):
                    kp = kxy[i]
                    vis = kv[i] if kv is not None else np.ones(3)
                    if len(kp) >= 3:
                        hx, hy = float(kp[0][0]), float(kp[0][1])
                        hv = int(vis[0] > 0.5)
                        tx, ty = float(kp[1][0]), float(kp[1][1])
                        tv = int(vis[1] > 0.5)
                        ax, ay = float(kp[2][0]), float(kp[2][1])
                        av = int(vis[2] > 0.5)

                rows.append(
                    {
                        "frame": frame_idx,
                        "track_id": int(track_id),
                        "confidence": float(conf),
                        "center_x": cx,
                        "center_y": cy,
                        "bbox_x1": float(x1),
                        "bbox_y1": float(y1),
                        "bbox_x2": float(x2),
                        "bbox_y2": float(y2),
                        "head_x": hx,
                        "head_y": hy,
                        "head_visible": hv,
                        "thorax_x": tx,
                        "thorax_y": ty,
                        "thorax_visible": tv,
                        "abdomen_x": ax,
                        "abdomen_y": ay,
                        "abdomen_visible": av,
                    }
                )

            if frame_idx % 5000 == 0 and total_frames > 0:
                print(f"  frames {frame_idx}/{total_frames}")

        print(f"done: {frame_idx} frames, {len(rows)} detection rows")

        if save_csv and rows:
            csv_path = output_dir / f"{video_path.stem}_tracking.csv"
            pd.DataFrame(rows).to_csv(csv_path, index=False)
            print(f"CSV: {csv_path}")
            return csv_path

        return None


def main() -> None:
    p = argparse.ArgumentParser(description="Fruit fly tracking (YOLO11m pose + ByteTrack)")
    p.add_argument("--video", required=True, help="Video file or directory if --batch")
    p.add_argument("--output", required=True, help="Output directory")
    p.add_argument(
        "--model",
        default=str(DEFAULT_MODEL),
        help=f"YOLO pose weights (default: {DEFAULT_MODEL})",
    )
    p.add_argument("--conf", type=float, default=0.28)
    p.add_argument("--iou", type=float, default=0.7)
    p.add_argument("--device", default="cuda:0", help='e.g. "cuda:0" or "cpu"')
    p.add_argument("--batch", action="store_true", help="Process all *.mp4 in --video dir")
    p.add_argument("--save-video", action="store_true", help="Placeholder for future annotated video export")
    args = p.parse_args()

    tracker = FlyTracker(Path(args.model), args.conf, args.iou, args.device)

    if args.batch:
        vdir = Path(args.video)
        for vf in sorted(vdir.glob("*.mp4")):
            sub = Path(args.output) / vf.stem
            tracker.process_video(vf, sub, save_video=args.save_video)
    else:
        tracker.process_video(Path(args.video), Path(args.output), save_video=args.save_video)


if __name__ == "__main__":
    main()
