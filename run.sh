#!/usr/bin/env bash
# 사용법: ./run.sh <pdf_path_or_filename> [extract_aio.py에 넘길 추가 옵션...]
#   ./run.sh my_paper.pdf                # papers/my_paper.pdf 자동 인식
#   ./run.sh papers/my_paper.pdf
#   ./run.sh papers/my_paper.pdf --model gemini-2.5-pro
#
# - conda 환경(hypergraphrag) 자동 활성화
# - .env(GEMINI_API_KEY) 존재 확인
# - 결과를 outputs/<pdf파일명>.json 에 자동 저장 (stdout에도 안내만 출력)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -z "${1:-}" ]; then
  echo "Usage: ./run.sh <pdf_path_or_filename> [extra extract_aio.py args...]" >&2
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

PDF_ARG="$1"
shift

if [ -f "$PDF_ARG" ]; then
  PDF_PATH="$PDF_ARG"
elif [ -f "$SCRIPT_DIR/papers/$PDF_ARG" ]; then
  PDF_PATH="$SCRIPT_DIR/papers/$PDF_ARG"
else
  echo "[ERROR] PDF를 찾을 수 없습니다: $PDF_ARG (papers/ 폴더도 확인했습니다)" >&2
  exit 1
fi

OUT_DIR="$SCRIPT_DIR/outputs"
mkdir -p "$OUT_DIR"
BASENAME="$(basename "$PDF_PATH")"
BASENAME="${BASENAME%.pdf}"
OUT_FILE="$OUT_DIR/${BASENAME}.json"

echo "[RUN] $PDF_PATH -> $OUT_FILE"
python "$SCRIPT_DIR/extract_aio.py" --pdf "$PDF_PATH" --output "$OUT_FILE" "$@"
echo "[DONE] Output saved to $OUT_FILE"
