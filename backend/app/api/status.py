import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import Job, JobStage, JobStatus

router = APIRouter()


class JobResponse(BaseModel):
    job_id: uuid.UUID
    title: str | None
    status: JobStatus
    stage: JobStage
    meta: dict


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: uuid.UUID, db: Session = Depends(get_session)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse(
        job_id=job.id,
        title=job.title,
        status=job.status,
        stage=job.stage,
        meta=job.meta or {},
    )
