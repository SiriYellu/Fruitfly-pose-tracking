# Setup & installation

## Python environment

Prefer **Python 3.11**:

```bash
python -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt
```

Adjust CUDA wheel index (`cu126`, `cu121`, CPU-only, etc.) to match host drivers.

Smoke test inference:

```bash
python examples/load_and_infer.py
```

## Troubleshooting

| Problem | Typical fix |
|---------|-------------|
| Out of VRAM tracking long videos | Stream mode already invoked; shrink resolution offline or `--device cpu` temporarily |
| `libGL` errors on servers | Install OpenCV headless extras or `opencv-python-headless` if replacing core wheel |
| Version skew with Ultralytics upgrade | Align `requirements.txt` upper bound intentionally |
