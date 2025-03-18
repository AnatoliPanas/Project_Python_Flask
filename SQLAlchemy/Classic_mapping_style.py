# Classic mapping style
from sqlalchemy import Table, Column, String, Text, Numeric, create_engine, Integer
from sqlalchemy.orm import registry, declarative_base

Base = declarative_base()

sqla_engine = create_engine(url="sqlite:///example.db",
                            echo=True,
                            echo_pool=True
                            # pool_size=10, #на sqlite3 не сработает
                            # max_overflow=10 #на sqlite3 не сработает
                            )

Register = registry()
metadata = Register.metadata

news_table = Table('news', metadata,
                   Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('title', String(50), unique=True),
                   Column('description', Text, nullable=True),
                   Column('rating', Numeric(3, 2)))


class News:
    def __init__(self, title, description, rating):
        self.title = title
        self.description = description
        self.rating = rating


Register.map_imperatively(News, news_table)
Register.metadata.create_all(bind=sqla_engine)