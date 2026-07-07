"""
LLM API 호출부. JooKyung/AIO-System/Layer 1/test_gemini/main.py 를 참고해
OpenAI 형식 대신 Gemini(google-genai) 형식으로 호출한다.

유지한 것:
- API key 로드 (.env의 GEMINI_API_KEY, 필요 시 인자로 override) - test_gemini와 동일하게 dotenv 사용
- model / temperature 등 기본 파라미터
- system prompt + (user prompt 텍스트 and/or PDF 문서) -> LLM 호출 -> raw response text 반환

PDF는 별도 텍스트 추출 없이, Gemini에 파일 바이트를 그대로 문서 파트로 전달한다
(Gemini가 PDF 레이아웃/표/그림까지 직접 이해하므로 텍스트 추출보다 정확도가 높다).
"""

import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).resolve().parent / ".env")

DEFAULT_MODEL = "gemini-3-flash-preview"
DEFAULT_TEMPERATURE = 0.0
# 이보다 낮은 기본값(미지정 시 8192)에 걸려 응답이 중간에 잘리는 것을 막기 위해
# 명시적으로 최대치를 요청한다.
DEFAULT_MAX_OUTPUT_TOKENS = 65536


def generate(
    system_prompt: str,
    user_prompt: str = "",
    pdf_bytes: bytes = None,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS,
    api_key: str = None,
):
    """system prompt + (user prompt text and/or PDF)를 조합해 LLM에 한 번 요청하고
    genai의 raw GenerateContentResponse를 그대로 반환한다 (text/usage/finish_reason 모두 필요할 때 사용)."""
    client = genai.Client(api_key=api_key)  # api_key=None이면 GEMINI_API_KEY 환경변수 사용

    contents = []
    if pdf_bytes is not None:
        contents.append(types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"))
    if user_prompt:
        contents.append(user_prompt)
    if not contents:
        raise ValueError("user_prompt 또는 pdf_bytes 중 하나는 반드시 있어야 합니다.")

    config = types.GenerateContentConfig(
        system_instruction=system_prompt or None,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )

    return client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )


def generate_with_retry(max_attempts=3, retry_backoff_seconds=5, **kwargs):
    """generate()를 호출하고, 네트워크/일시적 오류(레이트리밋 등)에 한해 재시도한다. JSON
    파싱 문제는 호출 자체의 실패가 아니라 응답 내용의 문제라서(salvage로 별도 처리) 여기서
    재시도 대상이 아니다. extract_aio.py/assemble_global.py가 공용으로 쓴다."""
    last_err = None
    for attempt in range(1, max_attempts + 1):
        try:
            return generate(**kwargs)
        except Exception as e:  # 네트워크/레이트리밋 등 일시적 오류
            last_err = e
            if attempt < max_attempts:
                print(f"    [WARN] API call failed (attempt {attempt}/{max_attempts}): {e}. Retrying in {retry_backoff_seconds}s...", file=sys.stderr)
                time.sleep(retry_backoff_seconds)
    raise last_err


def call_llm(
    system_prompt: str,
    user_prompt: str = "",
    pdf_bytes: bytes = None,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS,
    api_key: str = None,
) -> str:
    """generate()를 호출하고 raw response text만 반환하는 하위호환용 헬퍼."""
    response = generate(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        pdf_bytes=pdf_bytes,
        model=model,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        api_key=api_key,
    )
    return response.text or ""
