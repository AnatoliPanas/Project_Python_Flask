from sqlalchemy.orm import Mapped, mapped_column
from padv_9.models import db
# from padv_9.models.questions import Question


class Category(db.Model):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(
        db.Integer,
        db.Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(db.String(100), nullable=True)

    question: Mapped['Question'] = db.relationship('Question', back_populates='category')