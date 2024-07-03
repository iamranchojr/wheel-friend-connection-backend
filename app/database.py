from sqlmodel import create_engine, Session

from . import auth
from .config import get_database_url

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28
from .models import *


# create database engine
engine = create_engine(get_database_url())


def init_db() -> None:
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
