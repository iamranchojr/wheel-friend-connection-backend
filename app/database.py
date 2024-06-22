from sqlmodel import create_engine, SQLModel, Session, select
from .models import *

# from . import config

# create database engine
# engine = create_engine(config.get_settings().postgres_database_url)  # TODO: use env value
engine = create_engine('postgresql://postgres:postgres@db:5432/friend_connection_backend_db')


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
            statement = select(Friend).join(User, onclause=Friend.sender_id == User.id)
            print(statement)
            results = session.exec(statement)
            for f in results:
                print(f'Friend: {f.sender}')
