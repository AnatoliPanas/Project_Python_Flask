from sqlalchemy.orm import Mapped, mapped_column

from padv_9.models import db
# from padv_9.models.answers import Answer
# from padv_9.models.category import Category


class Question(db.Model):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(
        db.Integer,
        db.Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    text: Mapped[str] = mapped_column(
        db.String(255),
    )
    category_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('categories.id'))

    answers: Mapped[list['Answer']] = db.relationship('Answer', back_populates='question')
    category: Mapped['Category'] = db.relationship('Category', back_populates='question')

    def __repr__(self):
        return f'Question: {self.text}'


class Statistic(db.Model):
    __tablename__ = 'statistics'

    question_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('questions.id'),
        primary_key=True
    )
    agree_count: Mapped[int] = mapped_column(
        db.Integer,
        default=0
    )
    disagree_count: Mapped[int] = mapped_column(
        db.Integer,
        default=0
    )

    def __repr__(self):
        return '<Statistic for Question {}: {} agree, {} disagree>'.format(
            self.question_id,
            self.agree_count,
            self.disagree_count
        )
