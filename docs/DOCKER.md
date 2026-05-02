## Docker — reproducible environments

### GPU prerequisites

1. [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
2. Docker with Compose v2
3. Smoke test:  
   `docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi`

### Build

```bash
docker compose build gpu
docker compose build cpu-smoke
```

### Interactive shell

```bash
docker compose run --rm --gpus all gpu bash
python examples/load_and_infer.py
```

### Training

`gpu-train` wraps `scripts/train_scaled_model.py`.

- **Smoke defaults**: `EPOCHS=10`, `IMG_SIZE=640`, `BATCH=2` (fast sanity check).

```bash
docker compose run --rm --gpus all gpu-train
```

Compose typically requires **`--gpus all`** manually if your Compose file does not request devices (see Compose GPU docs).

- **Heavier reproduction** toward production settings:

```bash
EPOCHS=200 IMG_SIZE=2448 BATCH=4 docker compose run --rm --gpus all gpu-train
```

Artifacts appear under `./runs/train/` on the host.

### Inference / tracking

If `VIDEO` is unset, the container uses the small bundled demo:

`/workspace/results/tracked_videos/sample_pose_bytetrack_preview_720p.mp4`

```bash
docker compose run --rm --gpus all gpu-track
```

Custom clip (mount under `data/external_videos/` on host):

```bash
VIDEO=/videos/my_clip.mp4 docker compose run --rm --gpus all gpu-track
```

### CPU image (no NVIDIA)

```bash
docker compose run --rm cpu-smoke
```

Enough to verify installs and [`examples/load_and_infer.py`](../examples/load_and_infer.py); impractical for 2448 training.

### Pinned stacks

| File | Purpose |
|------|---------|
| `requirements-docker.txt` | Pinned Ultralytics stack on top of base PyTorch |
| `Dockerfile.gpu` | Pins **PyTorch 2.4.1 + CUDA 12.1 + cuDNN 9** via official `pytorch/pytorch` |

### Troubleshooting

| Symptom | Fix |
|---------|-----|
| DataLoader workers crash | Raise `shm_size` in `docker-compose.yml` beyond 8g if needed |
| CUDA OOM | Lower `BATCH` or `IMG_SIZE` |
| GPU not visible | Add `--gpus all` after `docker compose run` |
