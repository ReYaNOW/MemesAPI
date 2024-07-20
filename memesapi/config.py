from pydantic import HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    database_url: PostgresDsn

    main_server_url: HttpUrl
    private_server_url: HttpUrl

    minio_server_endpoint: str
    minio_root_user: str
    minio_root_password: str

    model_config = {'env_file': '.env'}


config = Config()
