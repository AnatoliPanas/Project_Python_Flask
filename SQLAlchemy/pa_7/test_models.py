from typing import List

from sqlalchemy import Column, DateTime, Float, ForeignKeyConstraint, Index, Integer, String, Text, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Roles(Base):
    __tablename__ = 'roles'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(20), nullable=False)

    users: Mapped[List['Users']] = relationship('Users', uselist=True, back_populates='role')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE', name='users_ibfk_1'),
        Index('ix_users_email', 'email'),
        Index('role_id', 'role_id'),
        Index('users_unique_email', 'email', unique=True)
    )

    id = mapped_column(Integer, primary_key=True)
    first_name = mapped_column(String(25), nullable=False)
    last_name = mapped_column(String(75), nullable=False)
    email = mapped_column(String(75), nullable=False)
    password = mapped_column(String(255), nullable=False)
    role_id = mapped_column(Integer, nullable=False)
    rating = mapped_column(Float, nullable=False, server_default=text("'0'"))
    deleted = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"))
    created_at = mapped_column(DateTime, nullable=False, server_default=text('(now())'))
    phone = mapped_column(String(30))
    updated_at = mapped_column(DateTime)
    deleted_at = mapped_column(DateTime)

    role: Mapped['Roles'] = relationship('Roles', back_populates='users')
    news: Mapped[List['News']] = relationship('News', uselist=True, back_populates='author')
    comments: Mapped[List['Comments']] = relationship('Comments', uselist=True, back_populates='author')


class News(Base):
    __tablename__ = 'news'
    __table_args__ = (
        ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='CASCADE', name='news_ibfk_1'),
        Index('author_id', 'author_id')
    )

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(75), nullable=False)
    body = mapped_column(Text, nullable=False)
    author_id = mapped_column(Integer, nullable=False)
    moderated = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"))
    deleted = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"))
    created_at = mapped_column(DateTime, nullable=False, server_default=text('(now())'))
    updated_at = mapped_column(DateTime)
    deleted_at = mapped_column(DateTime)

    author: Mapped['Users'] = relationship('Users', back_populates='news')
    comments: Mapped[List['Comments']] = relationship('Comments', uselist=True, back_populates='news')


class Comments(Base):
    __tablename__ = 'comments'
    __table_args__ = (
        ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='CASCADE', name='comments_ibfk_1'),
        ForeignKeyConstraint(['news_id'], ['news.id'], ondelete='CASCADE', name='comments_ibfk_2'),
        Index('author_id', 'author_id'),
        Index('news_id', 'news_id')
    )

    id = mapped_column(Integer, primary_key=True)
    body = mapped_column(Text, nullable=False)
    author_id = mapped_column(Integer, nullable=False)
    news_id = mapped_column(Integer, nullable=False)
    deleted = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"))
    created_at = mapped_column(DateTime, nullable=False, server_default=text('(now())'))
    updated_at = mapped_column(DateTime)
    deleted_at = mapped_column(DateTime)

    author: Mapped['Users'] = relationship('Users', back_populates='comments')
    news: Mapped['News'] = relationship('News', back_populates='comments')
