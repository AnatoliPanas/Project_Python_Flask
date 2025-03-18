from sqlalchemy import create_engine, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, sessionmaker

URL="sqlite:///:memory:"
sql_engine = create_engine(url=URL,
                           echo_pool=True,
                           echo=True)

Base = declarative_base()

class Category(Base):
    __tablename__ = "categorys"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(String(250))

    product: Mapped['Product'] = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(8,2))
    in_stock: Mapped[bool] = mapped_column(Boolean)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categorys.id'))

    category: Mapped['Category'] = relationship("User", back_populates="product")

Base.metadata.create_all(bind=sql_engine)

SessionFabric = sessionmaker(bind=sql_engine)
session = SessionFabric()
session.close()