from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id")
    )

    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("assessments.id")
    )

    score: Mapped[int] = mapped_column(Integer)

    skill_level: Mapped[int] = mapped_column(Integer)

    attempted_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )