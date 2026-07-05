"""
HyperGraphRAG에서 hypergraph 구축/저장/검색/청크 분할 로직을 모두 제거하고
"프롬프트 + 입력(텍스트 또는 PDF) -> LLM 호출 -> raw response 출력"만 남긴 최소 스크립트.
LLM은 Gemini(google-genai)를 사용한다.

사용 예:
    python extract_aio.py --pdf papers/2409.16118v3.pdf
    python extract_aio.py --pdf papers/2409.16118v3.pdf --output result.json
    python extract_aio.py --input paper_chunk.txt
    python extract_aio.py --text "some text" --model gemini-2.5-pro --temperature 0
"""

import argparse
import json
import sys
from pathlib import Path

from llm_client import call_llm, DEFAULT_MODEL, DEFAULT_TEMPERATURE

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SYSTEM_PROMPT_PATH = SCRIPT_DIR / "prompts" / "system_prompt.txt"
DEFAULT_USER_TEMPLATE_PATH = SCRIPT_DIR / "prompts" / "user_prompt_template.txt"


def parse_args():
    parser = argparse.ArgumentParser(description="Minimal Gemini call for n-ary relation / AIO extraction experiments.")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--pdf", type=str, help="입력 논문 PDF 파일 경로 (텍스트 추출 없이 Gemini에 그대로 전달)")
    input_group.add_argument("--input", type=str, help="입력 텍스트 파일 경로")
    input_group.add_argument("--text", type=str, help="입력 텍스트를 직접 문자열로 전달")

    parser.add_argument("--output", type=str, default=None, help="LLM raw response를 저장할 파일 경로 (생략 시 stdout 출력)")
    parser.add_argument("--system-prompt", type=str, default=str(DEFAULT_SYSTEM_PROMPT_PATH), help="SYSTEM 프롬프트 파일 경로")
    parser.add_argument("--user-prompt-template", type=str, default=str(DEFAULT_USER_TEMPLATE_PATH), help="USER 프롬프트 템플릿 파일 경로 ({text} 자리에 입력 텍스트 삽입, --pdf 사용 시 {text} 자리는 비워짐)")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--api-key", type=str, default=None, help="GEMINI_API_KEY를 인자로 직접 override (생략 시 .env/환경변수 사용)")
    return parser.parse_args()


def build_user_prompt(args, input_text: str = None) -> str:
    template = Path(args.user_prompt_template).read_text(encoding="utf-8")
    return template.replace("{text}", input_text if input_text is not None else "")


def main():
    args = parse_args()

    system_prompt = Path(args.system_prompt).read_text(encoding="utf-8")

    pdf_bytes = None
    if args.pdf:
        pdf_bytes = Path(args.pdf).read_bytes()
        user_prompt = build_user_prompt(args, input_text=None).strip()
    else:
        input_text = args.text if args.text is not None else Path(args.input).read_text(encoding="utf-8")
        user_prompt = build_user_prompt(args, input_text=input_text)

    raw_response = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        pdf_bytes=pdf_bytes,
        model=args.model,
        temperature=args.temperature,
        api_key=args.api_key,
    )

    # 최소한의 파싱 시도: 성공/실패 여부만 stderr에 알리고, raw response는 그대로 출력/저장한다.
    # Gemini가 ```json ... ``` 코드펜스로 감싸는 경우가 있어 파싱 체크에서만 벗겨낸다.
    stripped = raw_response.strip()
    if stripped.startswith("```"):
        stripped = stripped.split("\n", 1)[1] if "\n" in stripped else ""
        stripped = stripped.rsplit("```", 1)[0].strip()
    try:
        parsed = json.loads(stripped)
        item_count = len(parsed) if isinstance(parsed, list) else 1
        print(f"[INFO] JSON parse OK ({item_count} item(s)).", file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f"[WARN] JSON parse failed ({e}). Raw response is still saved/printed as-is.", file=sys.stderr)

    if args.output:
        Path(args.output).write_text(raw_response, encoding="utf-8")
        print(f"[INFO] Raw response written to {args.output}", file=sys.stderr)
    else:
        print(raw_response)


if __name__ == "__main__":
    main()
