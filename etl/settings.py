from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    """Settings for Postgres connection."""
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = ...
    password: str = ...
    host: str = ...
    port: int = ...

    class Config:
        env_prefix = 'postgres_'
        env_file = '../.env'
        env_file_encoding = 'utf-8'


class ElasticSearchSettings(BaseSettings):
    """Settings for ElasticSearch connection."""
    host: str = ...
    port: int = ...

    class Config:
        env_prefix = 'es_'
        env_file = '../.env'
        env_file_encoding = 'utf-8'


database_settings = PostgresSettings()
es_settings = ElasticSearchSettings()
