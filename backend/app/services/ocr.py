from typing import List, Protocol

from tenacity import retry, stop_after_attempt, wait_fixed


class SlideText(dict):
    pass


class OCRAdapter(Protocol):
    def extract(self, frame_paths: List[str]) -> List[SlideText]:
        ...


class MockOCRAdapter:
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def extract(self, frame_paths: List[str]) -> List[SlideText]:
        return [
            {"timestamp": 0.0, "text": "Sample slide text for mock OCR."}
        ]


def get_ocr_adapter() -> OCRAdapter:
    return MockOCRAdapter()
