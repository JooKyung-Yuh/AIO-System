#!/usr/bin/env bash
# 사용법: ./run_global.sh <run_dir> [<run_dir> ...] [assemble_global.py에 넘길 추가 옵션(생략 가능)...]
#   ./run_global.sh outputs/paperA_20260101_000000 outputs/paperB_20260101_000100
#   ./run_global.sh --all                # outputs/ 아래의 모든 Stage 1 run_dir을 자동으로 찾아 사용
#   ./run_global.sh outputs/paperA_... --max-nodes-per-batch 150   # pool이 너무 커서 한 번에 안 될 때
#
# Stage 2(assemble_global.py): run.sh(Stage 1)로 미리 추출해둔 논문별 run_dir들을 모아
# 전역 canonicalization + factor 조립을 수행한다. run.sh를 먼저 논문마다 실행해둬야 한다.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -z "${1:-}" ]; then
  echo "Usage: ./run_global.sh <run_dir> [<run_dir> ...] [extra assemble_global.py args...]" >&2
  echo "       ./run_global.sh --all   (outputs/ 아래 모든 Stage 1 run_dir을 자동으로 사용)" >&2
  exit 1
fi

if [ "${CONDA_DEFAULT_ENV:-}" != "hypergraphrag" ]; then
  if command -v conda >/dev/null 2>&1; then
    eval "$(conda shell.bash hook)"
    conda activate hypergraphrag
  fi
fi

if [ ! -f "$SCRIPT_DIR/.env" ]; then
  echo "[ERROR] $SCRIPT_DIR/.env 가 없습니다. GEMINI_API_KEY=... 한 줄을 넣어주세요." >&2
  exit 1
fi

if [ "$1" = "--all" ]; then
  shift
  echo "[RUN] assemble_global.py --outputs-dir outputs $*"
  python "$SCRIPT_DIR/assemble_global.py" --outputs-dir "$SCRIPT_DIR/outputs" "$@"
  exit 0
fi

echo "[RUN] assemble_global.py --run-dirs $* "
python "$SCRIPT_DIR/assemble_global.py" --run-dirs "$@"
