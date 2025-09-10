import os, glob, re, time, random
import cv2

# ================== CONFIG ==================
ROOT_DIR = r"C:\Users\siriy\Kennesaw State University\Dal Hyung Kim - 2023 FlyVialImage_Data"
OUT_DIR  = r"C:\Users\siriy\Kennesaw State University\Extracted_Frames_task"
FRAMES_PER_RUN = 80          # <- set 80 to get ~240 total (3 runs × 80)
RANDOM_SEED = 42             # set for reproducibility
VIDEO_EXTS = (".mp4", ".mov", ".avi", ".mkv")
# ============================================

os.makedirs(OUT_DIR, exist_ok=True)
random.seed(RANDOM_SEED)

def list_run_folders(root):
    # a "run" is any subfolder directly under ROOT_DIR whose name starts with "run "
    runs = []
    for name in os.listdir(root):
        p = os.path.join(root, name)
        if os.path.isdir(p) and name.lower().startswith("run"):
            runs.append(p)
    runs.sort()
    return runs

def find_segments(run_folder):
    segs = []
    for ext in VIDEO_EXTS:
        segs += glob.glob(os.path.join(run_folder, f"*{ext}"))
    # filter out tiny placeholders / non-local files if any
    segs = [s for s in segs if os.path.getsize(s) >= 1024]
    segs.sort()
    return segs

def safe_open_capture(p):
    cap = cv2.VideoCapture(p, cv2.CAP_FFMPEG)
    t0 = time.time()
    # retry up to 5s (helps with OneDrive latency)
    while not cap.isOpened() and time.time() - t0 < 5:
        time.sleep(0.25)
        cap.open(p)
    return cap

def choose_segment_indices(n, k):
    """Evenly spread k picks over n segments (allows repeats when k>n)."""
    if k <= 1:
        return [0 if n else []]
    if n <= 1:
        return [0]*k
    idxs = [round(i * (n - 1) / (k - 1)) for i in range(k)]
    return idxs

def main():
    runs = list_run_folders(ROOT_DIR)
    if not runs:
        print(f"No 'run *' folders found under: {ROOT_DIR}")
        return

    print(f"Found {len(runs)} run(s):")
    for r in runs:
        print(" -", os.path.basename(r))
    print()

    total_saved = 0
    for run in runs:
        run_name = os.path.basename(run)
        segs = find_segments(run)
        if not segs:
            print(f"⏭️ {run_name}: no video segments found, skipping")
            continue

        print(f"{run_name}: {len(segs)} segment file(s) found")
        k = FRAMES_PER_RUN
        idxs = choose_segment_indices(len(segs), k)

        saved_this_run = 0
        for pick_i, seg_idx in enumerate(idxs, start=1):
            seg = segs[seg_idx]
            cap = safe_open_capture(seg)
            if not cap.isOpened():
                print(f"   ❌ cannot open: {os.path.basename(seg)}")
                continue

            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
            if total <= 2*int(fps):
                cap.release()
                print(f"   ⏭️ too few frames in: {os.path.basename(seg)}")
                continue

            margin = int(fps)  # 1s margin
            lo = margin
            hi = max(margin+1, total - margin - 1)
            fi = random.randint(lo, hi)

            cap.set(cv2.CAP_PROP_POS_FRAMES, fi)
            ok, frame = cap.read()
            cap.release()
            if not ok:
                print(f"   ⏭️ read failed at frame {fi} in {os.path.basename(seg)}")
                continue

            # Build a clean prefix from run folder name (e.g., run 231127)
            base_prefix = run_name.replace(" ", "_")
            out_name = f"{base_prefix}_seg{seg_idx:03d}_frame{fi}.jpg"
            out_path = os.path.join(OUT_DIR, out_name)
            # ensure uniqueness in rare case
            suffix = 1
            while os.path.exists(out_path):
                out_name = f"{base_prefix}_seg{seg_idx:03d}_frame{fi}_{suffix}.jpg"
                out_path = os.path.join(OUT_DIR, out_name)
                suffix += 1

            cv2.imwrite(out_path, frame)
            saved_this_run += 1
            total_saved += 1

            if pick_i % 10 == 0 or pick_i == k:
                print(f"   … saved {saved_this_run}/{k}")

        print(f"✅ {run_name}: saved {saved_this_run}/{k} frames\n")

    print("=== Summary ===")
    print(f"Total runs processed: {len(runs)}")
    print(f"Total frames saved:   {total_saved}")
    print(f"Output folder:        {OUT_DIR}")

if __name__ == "__main__":
    main()
