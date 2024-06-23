from sqlmodel import create_engine, SQLModel, Session, select

from .config import settings
from .models import *


# create database engine
engine = create_engine(settings.DATABASE_URL)


def create_db_and_tables():
    """
    Creates the database and tables.
    """
    SQLModel.metadata.create_all(engine)
    _create_test_data()


def _create_test_data():
    with Session(engine) as session:
        if session.query(User).count() == 0:
            bob = User(
                name='Bob',
                email='bob@getwheel.io',
                username='bob@getwheel.io',
                hashed_password='somehashedpassword',
            )

            alice = User(
                name='Alice',
                email='alice@getwheel.io',
                username='alice@getwheel.io',
                hashed_password='somehashedpassword',
                status='Hi, I am Alice and it\'s nice to meet you'
            )

            session.add(bob)
            session.add(alice)
            session.commit()

            # create a friend object for bob and alice
            f = Friend(
                sender_id=bob.id,
                recipient_id=alice.id,
            )

            session.add(f)
            session.commit()

        else:
            statement = select(Friend)
            print(statement)
            results = session.exec(statement)
            for f in results:
                print(f'Friend: {f.id}, sender_id: {f.sender_id}, recipient_id: {f.recipient_id}')
