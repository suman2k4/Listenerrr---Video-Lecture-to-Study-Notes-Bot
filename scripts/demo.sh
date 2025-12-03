#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="infra/docker-compose.yml"

if ! command -v docker-compose >/dev/null 2>&1; then
  echo "docker-compose is required for the demo" >&2
  exit 1
fi

echo "Starting stack..."
docker-compose -f "$COMPOSE_FILE" up -d --build backend worker postgres redis minio createbuckets

sleep 5

echo "Triggering sample upload using curl"
JOB_ID=$(curl -s -X POST "http://localhost:8000/api/v1/upload" -F "title=Demo" -F "video_url=https://example.com/video.mp4" | jq -r '.job_id')

echo "Job queued: $JOB_ID"

echo "Waiting for completion..."
python - <<'PY'
import os
import time
import requests
job_id = os.environ["JOB_ID"]
for _ in range(20):
    resp = requests.get(f"http://localhost:8000/api/v1/jobs/{job_id}")
    data = resp.json()
    print(f"status={data['status']} stage={data['stage']}")
    if data["status"] in {"finished", "failed"}:
        break
    time.sleep(2)
PY

echo "Demo complete"
