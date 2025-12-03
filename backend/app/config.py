from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Central configuration loaded from environment variables."""

    app_name: str = "Listenerrr"
    api_prefix: str = Field("/api/v1", env="API_PREFIX")

    database_url: str = Field(
        "postgresql+psycopg://listenerrr:listenerrr@postgres:5432/listenerrr",
        env="POSTGRES_URL",
    )
    redis_url: str = Field("redis://redis:6379/0", env="REDIS_URL")

    minio_endpoint: str = Field("minio:9000", env="MINIO_ENDPOINT")
    minio_access_key: str = Field("listenerrr", env="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field("listenerrr123", env="MINIO_SECRET_KEY")
    minio_secure: bool = Field(False, env="MINIO_SECURE")
    minio_bucket: str = Field("listenerrr-artifacts", env="MINIO_BUCKET")

    whisper_mode: str = Field("mock", env="WHISPER_MODE")
    llm_mode: str = Field("mock", env="LLM_MODE")
    embeddings_mode: str = Field("mock", env="EMBEDDINGS_MODE")
    gemma_local_endpoint: str = Field(
        "http://localhost:11434/v1", env="GEMMA_LOCAL_ENDPOINT"
    )
    gemma_local_model: str = Field("gemma2:2b", env="GEMMA_LOCAL_MODEL")
    openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")
    gemini_api_key: str | None = Field(default=None, env="GEMINI_API_KEY")

    jwt_secret: str = Field("super-secret-change-me", env="JWT_SECRET")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    google_oauth_audience: str = Field("listenerrr", env="GOOGLE_OAUTH_AUDIENCE")

    celery_broker_url: str = Field("redis://redis:6379/1", env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(
        "redis://redis:6379/1", env="CELERY_RESULT_BACKEND"
    )
    celery_task_always_eager: bool = Field(False, env="CELERY_TASK_ALWAYS_EAGER")

    uploads_dir: str = Field("/app/storage/uploads", env="UPLOADS_DIR")
    outputs_dir: str = Field("/app/outputs", env="OUTPUTS_DIR")
    prompts_dir: str = Field("prompts", env="PROMPTS_DIR")
    faiss_workdir: str = Field("/app/outputs/search", env="FAISS_WORKDIR")

    upload_rate_per_minute: int = Field(5, env="UPLOAD_RATE_PER_MINUTE")
    share_token_bytes: int = Field(16, env="SHARE_TOKEN_BYTES")

    frontend_origin: str = Field("http://localhost:5173", env="FRONTEND_ORIGIN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
