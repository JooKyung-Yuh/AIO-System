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

from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).resolve().parent / ".env")

DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_TEMPERATURE = 0.0


def call_llm(
    system_prompt: str,
    user_prompt: str = "",
    pdf_bytes: bytes = None,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    api_key: str = None,
) -> str:
    """system prompt + (user prompt text and/or PDF)를 조합해 LLM에 한 번 요청하고 raw response text를 반환한다."""
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
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )
    return response.text
