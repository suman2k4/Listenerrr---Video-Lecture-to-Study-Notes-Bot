import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Protocol

import httpx
from tenacity import retry, stop_after_attempt, wait_fixed

from app.config import settings

PROMPTS_DIR = Path(settings.prompts_dir)
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)

"""Master Prompt Summary (condensed):
Transform lecture videos into structured study artifacts featuring summaries,
flashcards, semantic search, and downloadable formats while exposing both REST
APIs and a friendly web UI. Honor stage-level progress tracking, support
swappable adapters (mock/local/api) for Whisper, OCR, LLM, and embeddings, and
run background processing via Celery/Redis with PostgreSQL metadata storage and
MinIO artifact persistence."""


class LLMAdapter(Protocol):
    def structured_notes(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        ...

    def flashcards(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        ...


@lru_cache(maxsize=4)
def _load_prompt(name: str) -> str:
    path = PROMPTS_DIR / f"{name}.json"
    return path.read_text(encoding="utf-8")


class MockLLMAdapter:
    def structured_notes(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": payload.get("segment_transcript", "Segment")[:40],
            "bullets": [
                {
                    "time": payload.get("start_time", "00:00:00"),
                    "text": "Mock summary bullet",
                }
            ],
            "definitions": [],
            "formulas": [],
            "example": "Mock example",
            "tldr": "Mock TL;DR",
        }

    def flashcards(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "flashcards": [
                {
                    "q": "What does the mock adapter do?",
                    "a": "Returns deterministic flashcards.",
                }
            ]
        }


class GemmaLocalAdapter:
    def __init__(self) -> None:
        self.endpoint = settings.gemma_local_endpoint.rstrip("/")
        self.model = settings.gemma_local_model

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def _post(self, body: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.endpoint}/chat/completions"
        response = httpx.post(url, json=body, timeout=httpx.Timeout(60.0))
        response.raise_for_status()
        return response.json()

    def _invoke(
        self,
        system_prompt: str,
        payload: Dict[str, Any],
        fallback,
    ) -> Dict[str, Any]:
        body = {
            "model": self.model,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(payload)},
            ],
        }
        try:
            data = self._post(body)
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)
        except Exception as exc:  # pragma: no cover - network fallback path
            logger.warning("Gemma local invocation failed, falling back to mock: %s", exc)
            return fallback(payload)

    def structured_notes(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        prompt = _load_prompt("structured_notes")
        return self._invoke(prompt, payload, MOCK_ADAPTER.structured_notes)

    def flashcards(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        prompt = _load_prompt("flashcards")
        return self._invoke(prompt, payload, MOCK_ADAPTER.flashcards)


class PlaceholderRemoteAdapter:
    def __init__(self, provider: str) -> None:
        self.provider = provider

    def structured_notes(self, payload: Dict[str, Any]) -> Dict[str, Any]:  # pragma: no cover
        raise NotImplementedError(
            f"LLM_MODE={self.provider} requires implementation of provider-specific client"
        )

    def flashcards(self, payload: Dict[str, Any]) -> Dict[str, Any]:  # pragma: no cover
        raise NotImplementedError(
            f"LLM_MODE={self.provider} requires implementation of provider-specific client"
        )


MOCK_ADAPTER = MockLLMAdapter()


def get_llm_adapter() -> LLMAdapter:
    mode = (settings.llm_mode or "mock").lower()
    if mode == "mock":
        return MOCK_ADAPTER
    if mode == "gemma_local":
        return GemmaLocalAdapter()
    if mode == "openai":
        return PlaceholderRemoteAdapter("openai")
    if mode == "gemini":
        return PlaceholderRemoteAdapter("gemini")
    raise ValueError(f"Unsupported LLM_MODE '{settings.llm_mode}'")
