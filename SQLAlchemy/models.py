# Возможные варианты подключения к базам данных

# URI -> "<DBMS>+<library_name>://<user>:<password>@<host>:<port>/<database_name>"
#    "mysql+pymysql://root:rootpassword123@localhost:3306/my_database"
#    "sqlite:///<db_name>"

from sqlalchemy import create_engine, BigInteger, String, Integer, CheckConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, mapped_column, Mapped

Base = declarative_base()

sqla_engine = create_engine(url="sqlite:///example.db",
                            echo=True,
                            echo_pool=True
                            # pool_size=10, #на sqlite3 не сработает
                            # max_overflow=10 #на sqlite3 не сработает
                            )


# Declare style
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25), nullable=True)
    age: Mapped[int] = mapped_column(Integer, CheckConstraint('age > 0 AND age <= 120', name='age_check'))

Base.metadata.create_all(bind=sqla_engine)
SessionFabric = sessionmaker(bind=sqla_engine)
session = SessionFabric()

user = User(name="Anataoli2 Panas",
            age=39)

session.add(user)
session.commit()
session.close()
