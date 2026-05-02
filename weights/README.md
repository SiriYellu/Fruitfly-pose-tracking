# Model weights

| File | Description |
|------|--------------|
| `fruitfly_pose_yolo11m.pt` | Production **YOLO11m-Pose** weights (three keypoints: head, thorax, abdomen). Trained at full vial resolution; export name on disk was consolidated for this repo. |

**Approximate validation performance** (same run as `results/training_metrics.csv`, epoch 200):

- Pose mAP50 ≈ **0.985**
- Pose mAP50–95 ≈ **0.975**

See [`docs/05_training_and_metrics.md`](../docs/05_training_and_metrics.md) for how this checkpoint was produced and how metrics were logged.
