# Listenerrr — Video Lecture → Study Notes Bot

Transform lecture videos into searchable study artifacts with FastAPI, Celery, and a React front-end. This repo currently ships a mocked-but-runnable foundation so we can iterate quickly while bringing real ML adapters online.

## Features (current skeleton)
- FastAPI backend exposing `/api/v1/upload` and `/api/v1/jobs/{id}`.
- Celery worker that simulates the full pipeline and emits Markdown, PDF, flashcards, and a search index artifact.
- PostgreSQL schema managed via Alembic (initial `jobs` table with `JobStatus`/`JobStage` enums).
- Docker Compose stack for backend, worker, PostgreSQL, Redis, MinIO, and Vite frontend.
- Prompt templates, Postman collection, sample outputs, and demo script for rapid onboarding.
- Pytest suite with unit + integration coverage using Celery eager mode.

## Quick Start
1. Copy env vars:
   ```bash
   cp .env.example .env
   ```
2. Apply migrations:
   ```bash
   cd backend
   alembic upgrade head
   ```
3. Launch services:
   ```bash
   docker-compose -f infra/docker-compose.yml up --build
   ```
4. Visit `http://localhost:8000/docs` for OpenAPI or run `npm run dev` inside `frontend/` for the React UI.

## cURL Examples
```bash
# Upload using a URL
curl -X POST http://localhost:8000/api/v1/upload \
  -F "title=Linear Algebra Lecture" \
  -F "video_url=https://example.com/lecture.mp4"

# Check job status
curl http://localhost:8000/api/v1/jobs/<JOB_ID>
```

## Testing
```bash
cd backend
pytest --maxfail=1 --disable-warnings -q
```
Pytest swaps the DB for SQLite and forces `CELERY_TASK_ALWAYS_EAGER=true` so the mocked pipeline executes inline.

## Adapter Modes
- **LLM**: `LLM_MODE=gemma_local` (default) runs against a local Gemma-3 instance exposed via Ollama/vLLM on `http://localhost:11434/v1`. Switch to `mock` for CI or to unblock development, and reserve `openai` / `gemini` for forthcoming remote adapters. Override host/model via `GEMMA_LOCAL_ENDPOINT` and `GEMMA_LOCAL_MODEL`.
- **Whisper / Embeddings**: remain in `mock` until their respective adapters are implemented; the env values are already wired for quick swapping.

Every outbound call goes through a thin adapter layer so retry/timeouts + secret handling stay consistent regardless of provider.

## Project Layout
- `backend/` — FastAPI app, Celery worker, Alembic migrations, adapters.
- `frontend/` — Vite + React + Tailwind skeleton with upload + status views.
- `infra/docker-compose.yml` — Dev stack for API, worker, DB, Redis, MinIO, frontend.
- `prompts/` — Structured notes, flashcards, and segmenter templates required by LLM adapter.
- `tests/` — Pytest suites (unit + integration) using eager Celery.
- `docs/` — API reference plus future deployment notes.
- `samples/` — Example output for reference/fixtures.
- `scripts/demo.sh` — Boots services and runs a mocked upload via curl.

## Alembic Workflow
```bash
cd backend
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```
The first migration builds the `jobs` table with enum-backed status + stage columns.

## Security & Privacy Checklist (current status)
- Secrets sourced from env vars (`.env.example` documents each one).
- JWT secret placeholder included; replace before production.
- HTTPS termination + rate limiting + delete-user-data endpoint queued for upcoming sprints.

## Next Steps
1. Flesh out Whisper/OCR/LLM/Embedding adapters with retry + timeout wrappers.
2. Persist intermediate artifacts per pipeline step and wire semantic search.
3. Complete frontend views (notes viewer, auth stub) and analytics endpoints.
