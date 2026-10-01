from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id")
    )

    team_name: Mapped[str] = mapped_column(String(100))

    team_score: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30), default="generated"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )