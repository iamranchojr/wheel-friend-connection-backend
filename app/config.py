from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_database_url: str

    # TODD: figure out why .env file is not working
    model_config = SettingsConfigDict(env_file='../.env')


@lru_cache
def get_settings():
    """
    We are using a dependency to return the settings object.
    The usage of @lru_cache decorator on top is to make sure
    the object will be created only once the first time it's called.

    Read more here: https://fastapi.tiangolo.com/advanced/settings/#__tabbed_2_1
    :return: returns the settings object
    """
    return Settings()
