from typing import Type

from sqlalchemy import or_, not_, desc, func, and_, text

from SQLAlchemy.pa_7.models import User, Role, Comment, News
from SQLAlchemy.pa_7.db_connection import DBConnection
from SQLAlchemy.pa_7 import engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DataError


def create_new_role(session: Session, data: dict[str, str]) -> Role:
    try:
        role = Role(**data)  # Role(name="NEW ROLE")
        session.add(role)
        session.commit()  # Role(name="new role")
        session.refresh(role)

        return role
    except (IntegrityError, DataError) as err:
        session.rollback()
        raise err


def get_all_roles(session: Session) -> list[Type['Role']] | None:
    all_roles = session.query(Role).all()
    roles_by_name = session.query(Role.name)

    if all_roles:
        return all_roles


with DBConnection(engine) as session:
    #     role_data = {"name": "super_client"}
    #     new_role = create_new_role(session=session, data=role_data)
    #
    #     print(f"Объект успешно создан. Новая роль - {new_role.name}")

    roles = get_all_roles(session=session)
    for role in roles:
        print(f"Название роли - {role.name}")

    moderators_list = session.query(User).filter(User.role_id == 2).all()
    if moderators_list:
        for moder in moderators_list:
            print(f"{moder.email, moder.rating, moder.role_id}")

    all_authors_with_rating_gt_6: User = session.query(
        User.last_name,
        User.role_id,
        User.rating
    ).filter(
        User.role_id == 3,
        User.rating > 6,
        User.last_name.like("W%")
    )

    if all_authors_with_rating_gt_6:
        for user in all_authors_with_rating_gt_6:
            print(user.last_name, user.rating, user.role_id)

    users_with_rating_from_4_to_6 = session.query(
        User.email,
        User.rating
    ).filter(
        User.role_id == 3,
        User.rating.between(4, 6)
    ).all()

    for author in users_with_rating_from_4_to_6:
        print(author.email, author.rating)

    users_with_rating_from_4_to_6 = session.query(
        User.email,
        User.rating,
        User.first_name
    ).filter(
        or_(
            User.role_id == 3,
            User.rating.between(4, 6)
        ),
        not_(User.first_name.like("%n%"))
    ).order_by(desc(User.rating), User.first_name).all()

    for author in users_with_rating_from_4_to_6:
        print(author.email, author.rating, author.first_name)

    count_of_authors = session.query(
        func.count(User.id)
    ).filter(
        User.role_id == 3
    ).scalar()

    print(f"Count of author - {count_of_authors}")

    authors_by_rating = session.query(
        User.rating,
        func.count(User.id).label("count_of_authors")
    ).filter(
        User.role_id == 3
    ).group_by(User.rating).all()

    for us in authors_by_rating:
        print(us.rating, us.count_of_authors)

    avg_rating = session.query(
        func.avg(User.rating)
    ).filter(User.role_id == 3).scalar()

    authors_with_avg_rating = session.query(
        User.email, User.role_id, User.rating
    ).filter(User.rating >= avg_rating).all()

    for us in authors_with_avg_rating:
        print(us.email, us.role_id, us.rating)

    avg_rating1 = session.query(
        func.avg(User.rating)
    ).filter(User.role_id == 3).scalar_subquery()

    authors_with_avg_rating1 = session.query(
        User.email, User.role_id, User.rating
    ).filter(User.rating >= avg_rating).all()

    for us in authors_with_avg_rating1:
        print(us.email, us.role_id, us.rating)

    users_with_more_than_3_news = session.query(
        News.author_id,
        func.count(News.id).label("count_of_news")
    ).group_by(News.author_id).having(func.count(News.id) > 3).all()

    for us in users_with_more_than_3_news:
        print(us.author_id, us.count_of_news)

    author_id = session.query(
        Role.id
    ).filter(Role.name == "author").scalar_subquery()

    req_authors = session.query(
        User.id
    ).filter(
        User.role_id == author_id,
        User.rating > 6
    ).subquery()

    core_query = session.query(
        News.title,
        News.author_id,
        News.moderated
    ).filter(
        News.author_id.in_(req_authors),
    ).all()

    for n in core_query:
        print(n.title, n.author_id, n.moderated)

    news_info = session.query(
        News.title,
        News.moderated,
        News.author_id,
        User.rating
    ).join(User).filter(
        User.rating >= 6
    ).all()

    for n in news_info:
        print(n.title, n.moderated, n.author_id, n.rating)

    news_info = session.query(
        News.title,
        News.moderated,
        News.author_id,
        User.rating
    ).from_statement(
        text("""
            SELECT news.title, news.moderated, news.author_id, users.rating
            FROM news
            RIGHT JOIN users
            ON news.author_id = users.id
            WHERE users.rating >= 6
        """)
    ).all()

    for n in news_info:
        print(n.title, n.moderated, n.author_id, n.rating)
