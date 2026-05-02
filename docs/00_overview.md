# Project overview

The pipeline progresses from annotated vial imagery to pose estimation, temporal association with ByteTrack, optional geometric correction downstream, then behavioral aggregates.

Stages represented **in this repository**:

1. **Annotations** aligned with Roboflow YOLO-pose conventions (three keypoints per fly instance).
2. **Training** Ultralytics **YOLO11m-Pose** at native camera resolution regimes (see bundled metrics).
3. **Inference** exporting per-frame CSV (identity, bounding box extremes, pose coordinates).

Stages documented **conceptually only** due to artefact magnitude:

- Bulk curvature-correct mm trajectories spanning all clips.
- Professor-facing bout extraction MATLAB parity tooling.

Readers needing those massive CSV exports should coordinate storage per [`06_large_tracking_assets.md`](06_large_tracking_assets.md).
