from typing import List, Protocol

from tenacity import retry, stop_after_attempt, wait_fixed

from app.config import settings


class TranscriptChunk(dict):
    pass


class Transcriber(Protocol):
    def transcribe(self, audio_path: str) -> List[TranscriptChunk]:
        ...


class MockTranscriber:
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def transcribe(self, audio_path: str) -> List[TranscriptChunk]:
        return [
            {"start": 0.0, "end": 10.0, "text": "Welcome to Listenerrr mock transcript."}
        ]


def get_transcriber() -> Transcriber:
    mode = settings.whisper_mode
    if mode == "mock":
        return MockTranscriber()
    raise NotImplementedError(
        "Only mock mode is implemented in the skeleton. Configure WHISPER_MODE=mock."
    )
