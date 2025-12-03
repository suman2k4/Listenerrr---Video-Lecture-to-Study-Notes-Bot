"""Initial Job table

Revision ID: 20251202_0001
Revises:
Create Date: 2025-12-02 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision = "20251202_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    job_status = sa.Enum(
        "queued",
        "running",
        "finished",
        "failed",
        name="job_status",
    )
    job_stage = sa.Enum(
        "uploading",
        "extracting_audio",
        "transcribing",
        "ocr",
        "aligning",
        "segmenting",
        "summarizing",
        "indexing",
        "completed",
        name="job_stage",
    )
    job_status.create(op.get_bind(), checkfirst=True)
    job_stage.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "jobs",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("title", sa.String(length=255)),
        sa.Column("input_type", sa.String(length=32), nullable=False),
        sa.Column("input_location", sa.String(length=1024), nullable=False),
        sa.Column("status", job_status, nullable=False, server_default="queued"),
        sa.Column("stage", job_stage, nullable=False, server_default="uploading"),
        sa.Column("result_path", sa.String(length=1024)),
        sa.Column("meta", sa.JSON(), server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("jobs")
    sa.Enum(
        "queued",
        "running",
        "finished",
        "failed",
        name="job_status",
    ).drop(op.get_bind(), checkfirst=True)
    sa.Enum(
        "uploading",
        "extracting_audio",
        "transcribing",
        "ocr",
        "aligning",
        "segmenting",
        "summarizing",
        "indexing",
        "completed",
        name="job_stage",
    ).drop(op.get_bind(), checkfirst=True)
