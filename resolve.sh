#!/usr/bin/env bash
# 사용법: ./resolve.sh <run_dir> [output_path]
#   ./resolve.sh outputs/global_20260101_000000
#   ./resolve.sh outputs/global_20260101_000000 outputs/global_20260101_000000/readable.json
#
# LLM 호출 없이, result.json의 factor(node_id 참조)를 같은 run_dir의 <category>_canonicalized.json
# + observable_canonicalized.json과 매칭해 실제 text가 채워진 결과(result_resolved.json)를 만든다.
# run_global.sh(Stage 2) 실행 후, 또는 리팩터링 이전에 만들어진 단일-실행 run_dir에도 쓸 수 있다.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -z "${1:-}" ]; then
  echo "Usage: ./resolve.sh <run_dir> [output_path]" >&2
  exit 1
fi

RUN_DIR="$1"
OUTPUT="${2:-}"

if [ "${CONDA_DEFAULT_ENV:-}" != "hypergraphrag" ]; then
  if command -v conda >/dev/null 2>&1; then
    eval "$(conda shell.bash hook)"
    conda activate hypergraphrag
  fi
fi

if [ -n "$OUTPUT" ]; then
  python "$SCRIPT_DIR/resolve_factors.py" --run-dir "$RUN_DIR" --output "$OUTPUT"
else
  python "$SCRIPT_DIR/resolve_factors.py" --run-dir "$RUN_DIR"
fi
