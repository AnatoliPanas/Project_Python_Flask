from sqlalchemy import create_engine, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

# url="sqlite:///trening.db"
url="sqlite:///:memory:"
sqla_engine = create_engine(url=url,
                            echo=True,
                            echo_pool=True
                            # pool_size=10, #на sqlite3 не сработает
                            # max_overflow=10 #на sqlite3 не сработает
                            )

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    age: Mapped[int] = mapped_column(Integer)

    news: Mapped['News'] = relationship('News', back_populates="user")

class News(Base):
    __tablename__ = 'news'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(250))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    user: Mapped['User'] = relationship('User', back_populates="news")

Base.metadata.create_all(bind=sqla_engine)