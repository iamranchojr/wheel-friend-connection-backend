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
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8


settings = Settings()


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
