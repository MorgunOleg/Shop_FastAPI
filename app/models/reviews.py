from datetime import datetime, timezone

from sqlalchemy import Boolean, Integer, ForeignKey, Text, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    comment: Mapped[str | None] = mapped_column(Text)
    comment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                   default=lambda: datetime.now(timezone.utc))
    grade: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("grade >= 1 AND grade <= 5", name="check_grade_range"),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    buyer: Mapped["User"] = relationship("User", back_populates="reviews")
    product: Mapped["Product"] = relationship("Product", back_populates="reviews")
