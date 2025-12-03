# API Reference (Skeleton)

## POST /api/v1/upload
- **Description**: Queue a lecture for processing. Accepts either a file upload or an external video URL.
- **Body** (multipart/form-data):
  - `title` (optional string)
  - `video_url` (optional string)
  - `file` (optional file)
- **Response** (`202 Accepted`):
```json
{
  "job_id": "<uuid>",
  "status": "queued",
  "stage": "uploading"
}
```

## GET /api/v1/jobs/{job_id}
- **Description**: Retrieve the latest status, stage, and metadata for a job.
- **Response** (`200 OK`):
```json
{
  "job_id": "<uuid>",
  "title": "Lecture",
  "status": "finished",
  "stage": "completed",
  "meta": {
    "progress": [
      {"stage": "transcribing", "message": "Transcribing complete", "ts": 1700000000}
    ],
    "artifacts": {"notes_md": "/app/outputs/<id>/notes.md"}
  }
}
```
