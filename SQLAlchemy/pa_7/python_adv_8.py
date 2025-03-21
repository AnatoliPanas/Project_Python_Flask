import json
from datetime import datetime

from sqlalchemy import func, desc

from SQLAlchemy.pa_7 import engine
from SQLAlchemy.pa_7.db_connection import DBConnection
from SQLAlchemy.pa_7.models import User, News, Role


def print_model_fields(rows, model):
    columns = model.__table__.columns

    for row in rows:
        row_data = ", ".join([f"{column.name}: {getattr(row, column.name)}" for column in columns])
        print(row_data)


def get_model_fields(records, columns):
    # row_data = []
    # for rec in records:
    #     row_data.append(", ".join([f"{column.name}: {getattr(rec, column.name)}" for column in columns]))

    response_data = [
        {column.name: (
            getattr(rec, column.name).strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(getattr(rec, column.name), datetime)
            else getattr(rec, column.name)
        ) for column in columns}
        for rec in records
    ]

    return response_data


with (DBConnection(engine) as session):
    # ========================================>
    # author_mehr5 = session.query(User.id, User.last_name, User.rating, User.role_id).filter(
    #     User.rating > 5
    # ).all()
    #
    # columns = [User.id, User.last_name, User.rating, User.role_id]
    #
    # for item in get_model_fields(author_mehr5, columns):
    #     print(item)
    # <=======================================

    # ========================================>
    # news_list = session.query(News.title, News.moderated, News.deleted, News.author_id).filter(
    #     News.moderated == 0, News.deleted == 0
    # ).all()
    #
    # columns = [News.title, News.moderated, News.deleted, News.author_id]
    #
    # print(json.dumps(get_model_fields(news_list, columns), indent=4))
    # <=======================================

    # ========================================>
    # users_22 = session.query(User.last_name, User.created_at).filter(
    #     User.created_at.between(datetime(2022, 1, 1), datetime(2022, 12, 31))
    #
    # ).all()

    # response_data = [
    #     {
    #         "last_name": user.last_name,
    #         "created_at": datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
    #     }
    #     for user in users_22
    # ]
    #
    # print(json.dumps(response_data, indent=4))

    # columns = [User.last_name, User.created_at]
    #
    # print(json.dumps(get_model_fields(users_22, columns), indent=4))
    # <=======================================


    # all_users_with_role = session.query(
    #     User.last_name,
    #     User.email,
    #     Role.name.label("role_name")
    # ).join(User.role).all()
    #
    # for user in all_users_with_role:
    #     print(user.last_name, user.email, user.role_name)

    # ========================================>
    author = session.query(User.last_name,
                           User.email,
                           Role.name.label('name_role'),
                           User.rating,
                           func.count().label('cn')).join(
        User.role).join(User.news).group_by(User.last_name,
                                            User.email,
                                            Role.name,
                                            User.rating).order_by(desc(func.count())).first()

    print(author)