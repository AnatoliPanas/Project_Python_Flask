from sqlalchemy.orm import Mapped, mapped_column
from padv_9.models import db
# from padv_9.models.questions import Question


class Answer(db.Model):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(
        db.Integer,
        db.Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    question_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('questions.id'),
    )
    is_agree: Mapped[bool] = mapped_column(
        db.Boolean,
    )

    question: Mapped['Question'] = db.relationship('Question', back_populates='answers')

    def __repr__(self):
        return 'Statistic for Question {}: {} agree, {} disagree'.format(
            self.question_id,
            self.agree_count,
            self.disagree_count
        )
