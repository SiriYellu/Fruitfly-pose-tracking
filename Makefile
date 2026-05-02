# Makefile — optional shortcuts (Unix)
# Usage: make docker-build-gpu

.PHONY: docker-build-gpu docker-shell-gpu docker-train-sm docker-track-demo docker-cpu-smoke compose-check

docker-build-gpu:
	docker compose build gpu

docker-shell-gpu:
	docker compose run --rm --gpus all gpu bash

# Short training smoke (adjust EPOCHS/IMG_SIZE/BATCH on CLI)
docker-train-sm:
	docker compose run --rm --gpus all gpu-train

# Track using default bundled preview MP4
docker-track-demo:
	docker compose run --rm --gpus all gpu-track

docker-cpu-smoke:
	docker compose run --rm cpu-smoke

compose-check:
	docker compose config
