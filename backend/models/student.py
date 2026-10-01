from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True
    )

    roll_number: Mapped[str] = mapped_column(
        String(50), unique=True
    )

    branch: Mapped[str] = mapped_column(String(100))

    semester: Mapped[int] = mapped_column(Integer)

    cgpa: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    bio: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    availability_hours: Mapped[int] = mapped_column(
        Integer, default=10
    )