import secrets
# from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings object
    """
    # TODD: figure out why .env file is not working
    model_config = SettingsConfigDict(
        env_file='.env',
        env_ignore_empty=True,
        extra='ignore',
    )

    DATABASE_URL: str
    SECRET_KEY: str
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECURE_SSL_REDIRECT: bool = False


settings = Settings()


def get_database_url() -> str:
    database_url = settings.DATABASE_URL

    if database_url.startswith('postgres://'):
        # to get around issue with heroku postgres
        # https://stackoverflow.com/questions/52543783/connecting-heroku-database-to-sqlalchemy
        database_url = database_url.replace('postgres://', 'postgresql://')

    return database_url


# @lru_cache
# def get_settings():
#     """
#     We are using a dependency to return the settings object.
#     The usage of @lru_cache decorator on top is to make sure
#     the object will be created only once the first time it's called.
#
#     Read more here: https://fastapi.tiangolo.com/advanced/settings/#__tabbed_2_1
#     :return: returns the settings object
#     """
#     return Settings()
