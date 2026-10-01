from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class StudentSkill(Base):
    __tablename__ = "student_skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id")
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id")
    )

    level: Mapped[int] = mapped_column(Integer)
    source: Mapped[str] = mapped_column(
        String(30), default="self"
    )