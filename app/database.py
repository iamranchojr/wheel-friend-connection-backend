from sqlmodel import create_engine, SQLModel

# from . import config

# create database engine
# engine = create_engine(config.get_settings().postgres_database_url)
engine = create_engine('postgresql://postgres:postgres@db:5432/friend_connection_backend_db')


def create_db_and_tables():
    """
    Creates the database and tables.
    """
    SQLModel.metadata.create_all(engine)
