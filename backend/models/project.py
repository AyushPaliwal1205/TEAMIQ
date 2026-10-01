from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(200))

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    team_size: Mapped[int] = mapped_column(Integer)

    created_by: Mapped[int] = mapped_column(
        ForeignKey("students.id")
    )

    status: Mapped[str] = mapped_column(
        String(30), default="active"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    