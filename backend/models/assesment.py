from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    title: Mapped[str] = mapped_column(String(200))
    total_questions: Mapped[int] = mapped_column(Integer)
    passing_score: Mapped[int] = mapped_column(Integer)