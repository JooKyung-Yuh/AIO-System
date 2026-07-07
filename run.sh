#!/usr/bin/env bash
# 사용법: ./run.sh <pdf_path_or_filename> [extract_aio.py에 넘길 추가 옵션(생략 가능)...]
#   ./run.sh my_paper.pdf                # papers/my_paper.pdf 자동 인식, 기본값으로 바로 실행
#   ./run.sh papers/my_paper.pdf
#   ./run.sh papers/my_paper.pdf --model gemini-2.5-pro   # 필요할 때만 기본값을 override
#
# 이 스크립트는 Stage 1(논문 1편에서 evidence node 추출)만 실행한다. Stage 2(여러 논문을
# 가로지르는 전역 canonicalization + factor 조립)는 run_global.sh를 따로 실행한다 - 여러
# 논문을 이 스크립트로 각각 먼저 돌린 뒤, 그 run_dir들을 run_global.sh에 넘기면 된다.
#
# 매번 옵션을 직접 타이핑하지 않아도 되도록 아래 기본값을 이 파일 안에 고정해뒀다.
# 값을 바꾸고 싶으면 DEFAULT_* 변수를 수정하거나, 실행할 때 뒤에 옵션을 추가로 넘기면
# (extract_aio.py의 argparse는 같은 옵션이 두 번 오면 마지막 값을 쓰므로) 그 값으로 덮어써진다.
DEFAULT_PAGES_PER_CHUNK=6
DEFAULT_PAPER_TITLE_HINT="unknown"
# --model / --temperature / --max-output-tokens은 llm_client.py의 기본값(gemini-3-flash-preview,
# temperature 0.0, max_output_tokens 65536)을 그대로 쓴다. 바꾸고 싶으면 실행 시 뒤에
# --model ... 처럼 추가하면 된다.

# - conda 환경(hypergraphrag) 자동 활성화
# - .env(GEMINI_API_KEY) 존재 확인
# - 산출물은 outputs/<pdf파일명>_<KST 타임스탬프>/ 디렉터리에 남는다: 카테고리별 노드 json
#   (observable은 eval_metric+pattern으로 나뉜 observable.json), 청크별 원본 응답, metadata.
#   이 디렉터리 경로를 run_global.sh(Stage 2)에 넘기면 된다.
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
TIMESTAMP="$(TZ='Asia/Seoul' date +%Y%m%d_%H%M%S)"  # extract_aio.py 내부 run 디렉터리 이름과 동일하게 KST 기준
RUN_DIR="$OUT_DIR/${BASENAME}_${TIMESTAMP}"

echo "[RUN] $PDF_PATH -> $RUN_DIR"
python "$SCRIPT_DIR/extract_aio.py" \
  --pdf "$PDF_PATH" \
  --run-dir "$RUN_DIR" \
  --paper-id "$BASENAME" \
  --paper-title-hint "$DEFAULT_PAPER_TITLE_HINT" \
  --pages-per-chunk "$DEFAULT_PAGES_PER_CHUNK" \
  "$@"
echo "[DONE] Stage 1 output saved to $RUN_DIR"
echo "[NEXT] Run Stage 2 once all papers are extracted: ./run_global.sh $RUN_DIR [more run_dirs...]"
