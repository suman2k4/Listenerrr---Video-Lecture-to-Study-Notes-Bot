"""Add users table and extend jobs

Revision ID: 20251202_0002
Revises: 20251202_0001
Create Date: 2025-12-02 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


revision = "20251202_0002"
down_revision = "20251202_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.add_column(
        "jobs",
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
    )
    op.add_column("jobs", sa.Column("share_token", sa.String(length=64), nullable=False))
    op.add_column("jobs", sa.Column("artifacts", sa.JSON(), server_default=sa.text("'{}'::jsonb")))
    op.add_column("jobs", sa.Column("started_at", sa.DateTime(), nullable=True))
    op.add_column("jobs", sa.Column("completed_at", sa.DateTime(), nullable=True))
    op.add_column("jobs", sa.Column("duration_seconds", sa.Integer(), nullable=True))
    op.create_index("ix_jobs_share_token", "jobs", ["share_token"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_jobs_share_token", table_name="jobs")
    op.drop_column("jobs", "duration_seconds")
    op.drop_column("jobs", "completed_at")
    op.drop_column("jobs", "started_at")
    op.drop_column("jobs", "artifacts")
    op.drop_column("jobs", "share_token")
    op.drop_column("jobs", "user_id")
    op.drop_table("users")
