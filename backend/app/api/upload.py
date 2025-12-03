import shutil
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_session
from app.models import Job, JobStage, JobStatus
from app.workers.pipeline import run_pipeline

router = APIRouter()


class UploadJobResponse(BaseModel):
    job_id: uuid.UUID
    status: JobStatus
    stage: JobStage


def _persist_upload(job_id: uuid.UUID, upload: UploadFile) -> str:
    uploads_dir = Path(settings.uploads_dir)
    uploads_dir.mkdir(parents=True, exist_ok=True)
    dest_path = uploads_dir / f"{job_id}_{upload.filename}"
    with dest_path.open("wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)
    return str(dest_path)


@router.post("/", response_model=UploadJobResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_lecture(
    title: Optional[str] = Form(None),
    video_url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_session),
):
    if not file and not video_url:
        raise HTTPException(status_code=400, detail="Provide a file or video_url")

    job = Job(
        title=title,
        input_type="url" if video_url else "upload",
        input_location=video_url or "pending",
        status=JobStatus.queued,
        stage=JobStage.uploading,
        meta={"progress": []},
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    input_location = job.input_location
    if file:
        input_location = _persist_upload(job.id, file)
        job.input_location = input_location
        db.add(job)
        db.commit()

    run_pipeline.delay(str(job.id), input_location)

    return UploadJobResponse(job_id=job.id, status=job.status, stage=job.stage)
