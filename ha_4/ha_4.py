from sqlalchemy import (
    create_engine,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    Identity,
    func, Boolean, desc
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Mapped, mapped_column, Session
from sqlalchemy.exc import IntegrityError, DataError

from datetime import datetime

from ha_3 import Category


def get_model_fields(records, columns):
    response_data = []

    for rec in records:
        row = {}
        for column in columns:
            column_name = column if isinstance(column, str) else column.name
            value = getattr(rec, column_name)

            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif value is None:
                value = None

            row[column_name] = value

        response_data.append(row)

    return response_data


def insert_in_table(session: Session, datas):
    try:
        session.add_all(datas)
        session.commit()

        return datas
    except (IntegrityError, DataError) as err:
        session.rollback()
        raise err


Base = declarative_base()
URL = "sqlite:///ha_4.db"
# URL='sqlite:///:memory:'
engine = create_engine(url=URL, echo=True,
                       echo_pool=True)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(String(250))

    product: Mapped['Product'] = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(8, 2))
    in_stock: Mapped[bool] = mapped_column(Boolean)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'))

    category: Mapped['Category'] = relationship("Category", back_populates="product")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# сategorys = [Category(name="Электроника", description="Гаджеты и устройства."),
#              Category(name="Книги", description="Печатные книги и электронные книги."),
#              Category(name="Одежда", description="Одежда для мужчин и женщин.")
#              ]
# insert_in_table(session, сategorys)
#
# сategorys = [Product(name="Смартфон", price=299.99, in_stock=True, category_id=1),
#              Product(name="Ноутбук", price=499.99, in_stock=True, category_id=1),
#              Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category_id=2),
#              Product(name="Джинсы", price=40.50, in_stock=True, category_id=3),
#              Product(name="Футболка", price=20.00, in_stock=True, category_id=3)
#              ]
# insert_in_table(session, сategorys)

# -> Извлеките все записи из таблицы categories.
# Для каждой категории извлеките и выведите все связанные с
# ней продукты, включая их названия и цены.

all_catigorys = session.query(Category.id,
                              Category.name,
                              Category.description,
                              Product.name,
                              Product.price).join(Product.category).all()

if all_catigorys:
    columns = [Category.id,
               Category.name,
               Category.description,
               Product.name,
               Product.price]

    for rec in get_model_fields(all_catigorys, columns):
        print(rec)

# <-

# -> Найдите в таблице products первый продукт с названием "Смартфон".
# Замените цену этого продукта на 349.99.

try:
    product_smartfon = session.query(Product).filter(Product.name == "Смартфон").first()
    if product_smartfon:
        product_smartfon.price = 349.99
        session.commit()
except Exception as e:
    print(f"Произошла ошибка: {e}")
    session.rollback()

# <-

# -> Используя агрегирующие функции и группировку,
# подсчитайте общее количество продуктов в каждой категории.

count_product_from_category = ((session.query(Product.category_id,
                                              Category.name,
                                              func.count().label("cn")).
                                join(Category.product).
                                group_by(Product.category_id, Category.name)).
                               order_by(func.count()).all())

if count_product_from_category:
    columns = [Product.category_id,
               Category.name,
               'cn']

    for rec in get_model_fields(count_product_from_category, columns):
        print(rec)
# <-

# -> Отфильтруйте и выведите только те категории, в которых более одного продукта.

filtered_categories = ((session.query(Product.category_id,
                                              Category.name,
                                              func.count().label("cn")).
                                join(Category.product).
                                group_by(Product.category_id, Category.name)).
                                having(func.count() > 1).
                               order_by(func.count()).all())

if filtered_categories:
    columns = [Product.category_id,
               Category.name,
               'cn']

    for rec in get_model_fields(filtered_categories, columns):
        print(rec)
# <-

session.close()
