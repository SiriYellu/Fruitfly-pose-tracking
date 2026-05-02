# Stage 02 — Dataset, tracking config, and weights

**Goal:** Valid YOLO-pose **`data.yaml`**, inference defaults, and the production checkpoint.

| Path | Role |
|------|------|
| `dataset/yolo_pose/` | Minimal YOLO-format split + `data.yaml` (expand privately for serious training). |
| `configs/tracking.yaml` | Reference geometry / tracking-related defaults for experiments. |
| `weights/fruitfly_pose_yolo11m.pt` | Shipped production YOLO11m-Pose weights (~41 MB). |

**Next:** [`../stage_03_training/README.md`](../stage_03_training/README.md) · **Skip training:** jump to [`../stage_04_inference_tracking/README.md`](../stage_04_inference_tracking/README.md).

**Docs:** [`docs/02_data.md`](../../../docs/02_data.md).
