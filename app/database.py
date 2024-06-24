from sqlmodel import create_engine, SQLModel, Session

from . import auth
from .config import settings
from .models import *


# create database engine
database_url = settings.DATABASE_URL

if database_url.startswith('postgres://'):
    # to get around issue with heroku postgres
    # https://stackoverflow.com/questions/52543783/connecting-heroku-database-to-sqlalchemy
    database_url = database_url.replace('postgres://', 'postgresql://')

engine = create_engine(database_url)


def create_db_and_tables():
    """
    Creates the database and tables.
    """
    SQLModel.metadata.create_all(engine)
    _create_seed_data()


def _create_seed_data():
    with Session(engine) as session:
        if session.query(User).count() == 0:
            bob = User(
                name='Jose',
                email='jose@getwheel.io',
                username='jose@getwheel.io',
                bio='We are building something amazing at getwheel.io. Send a friend request to learn more',
                hashed_password=auth.get_password_hash('BOBPassword'),
            )

            alice = User(
                name='Alice',
                email='alice@getwheel.io',
                username='alice@getwheel.io',
                hashed_password=auth.get_password_hash('AlicePassword'),
                status='Hi, I am Alice and it\'s nice to meet you'
            )

            session.add(bob)
            session.add(alice)
            session.commit()

            # create a friend object for bob and alice
            # f = Friend(
            #     sender_id=bob.id,
            #     recipient_id=alice.id,
            # )

            # session.add(f)
            # session.commit()
