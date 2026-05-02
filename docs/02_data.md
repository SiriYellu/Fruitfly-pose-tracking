# Data conventions

Each detection instance annotates:

- Bounding box enclosing the animal.
- **Three keypoints** in order `[head, thorax, abdomen]`.
- Visibility flags conforming Ultralytics pose label encoding.

Minimal complete template lives under `pipeline/stages/stage_02_dataset_config_weights/dataset/yolo_pose/` with `train/`, `valid/`, `test/` partitions.

Starter Roboflow export is archived at `data/roboflow/roboflow_export_yolov8_pose.zip` — unzip externally and realign `paths` inside its `data.yaml` when relocating splits.
