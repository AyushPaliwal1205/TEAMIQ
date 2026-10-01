from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TeamMember(Base):
    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id")
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id")
    )

    role: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )