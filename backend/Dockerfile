FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /app/
COPY prompts/ /prompts/

ENV PROMPTS_DIR=/prompts

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
