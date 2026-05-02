#!/usr/bin/env bash
# Build GitHub-publishable artefacts from lab curvature CSVs:
# - 48 per-clip xz: Tracks_corrected_imgXXXX.csv.xz
# - dual merged split into LINE chunks (header repeated) + xz: dual_vial/Tracks_corr_dual_vial.partNN.csv.xz
set -euo pipefail

SRC_CLIP_DIR="${SRC_CLIP_DIR:-/mnt/storage5/Fruitfly/Traingagain/final_reportings/curvature-corrected tracking data}"
SRC_DUAL="${SRC_DUAL:-/mnt/storage5/Fruitfly/Traingagain/final_reportings/Combined tracking data/tracks_corrected_dual_vial.csv}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
OUT="${OUT:-$ROOT/data/run231127_github_release}"

LINES_PER_DUAL_CHUNK="${LINES_PER_DUAL_CHUNK:-1200000}"

mkdir -p "$OUT/per_clip" "$OUT/dual_vial"

echo "OUT=$OUT"
echo "Compressing $(ls "$SRC_CLIP_DIR"/tracks_corrected_clip*.csv 2>/dev/null | wc -l) clips with xz..."
while IFS= read -r -d '' f; do
  vid=$(awk -F, 'NR==2{print $2; exit}' "$f")
  img=$(echo "$vid" | grep -oE 'img[0-9]{4}')
  if [[ -z "${img:-}" ]]; then
    echo "WARN: skip $f bad video tag: $vid" >&2
    continue
  fi
  tgt="$OUT/per_clip/Tracks_corrected_${img}.csv.xz"
  echo " -> $tgt"
  xz -T0 -c "$f" > "$tgt.tmp" && mv "$tgt.tmp" "$tgt"
done < <(find "$SRC_CLIP_DIR" -maxdepth 1 -name 'tracks_corrected_clip*.csv' -print0 | sort -z)

echo "Splitting dual-vial CSV (~13 GB) — **header only on part 01** — then xz each shard (<100 MiB each)."
HEADER=$(head -1 "$SRC_DUAL")
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT
rm -f "$OUT"/dual_vial/Tracks_corr_dual_vial.part*.csv.xz
mkdir -p "$OUT/dual_vial"
tail -n +2 "$SRC_DUAL" | split -l "$LINES_PER_DUAL_CHUNK" -d -a 2 - "$tmpdir/body_"
first=1
n=1
for bf in $(ls "$tmpdir"/body_* 2>/dev/null | sort -V); do
  [[ -e "$bf" ]] || continue
  num=$(printf '%02d' "$n")
  tgt="$OUT/dual_vial/Tracks_corr_dual_vial.part${num}.csv.xz"
  echo " xz dual part $num"
  if [[ "$first" -eq 1 ]]; then
    { printf '%s\n' "$HEADER"; cat "$bf"; } | xz -T0 -c > "${tgt}.tmp" && mv "${tgt}.tmp" "$tgt"
    first=0
  else
    xz -T0 -c "$bf" > "${tgt}.tmp" && mv "${tgt}.tmp" "$tgt"
  fi
  rm -f "$bf"
  n=$((n+1))
done
rm -rf "$tmpdir"

echo "(cd '$OUT' && sha256sum per_clip/*.csv.xz dual_vial/*.csv.xz) > HASHES.sha256"
(cd "$OUT" && sha256sum per_clip/*.csv.xz dual_vial/*.csv.xz 2>/dev/null | sort > HASHES.sha256) || true
echo DONE
