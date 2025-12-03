from typing import List, Protocol

import numpy as np

from app.config import settings


class EmbeddingsAdapter(Protocol):
    def embed(self, texts: List[str]) -> List[List[float]]:
        ...


class MockEmbeddingsAdapter:
    def embed(self, texts: List[str]) -> List[List[float]]:
        return [[float(i) for i in np.linspace(0.1, 0.9, num=3)] for _ in texts]


def get_embeddings_adapter() -> EmbeddingsAdapter:
    if settings.embeddings_mode == "mock":
        return MockEmbeddingsAdapter()
    raise NotImplementedError("Only mock embeddings adapter is available in the skeleton")
