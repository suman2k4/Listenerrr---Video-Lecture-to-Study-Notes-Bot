import os
from pathlib import Path

os.environ.setdefault("POSTGRES_URL", "sqlite+pysqlite:///./listenerrr_test.db")
os.environ.setdefault("CELERY_TASK_ALWAYS_EAGER", "true")
os.environ.setdefault("UPLOADS_DIR", "./test_storage/uploads")
os.environ.setdefault("OUTPUTS_DIR", "./test_storage/outputs")

from app.database import engine  # noqa: E402
from app.models import Base  # noqa: E402

import pytest


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def prepare_dirs():
    Path(os.environ["UPLOADS_DIR"]).mkdir(parents=True, exist_ok=True)
    Path(os.environ["OUTPUTS_DIR"]).mkdir(parents=True, exist_ok=True)
    yield
