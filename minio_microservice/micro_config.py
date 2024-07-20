from pydantic import Extra, HttpUrl
from pydantic_settings import BaseSettings


class Config(BaseSettings, extra=Extra.allow):
    host: str = '0.0.0.0'
    private_server_url: HttpUrl
    workers: int = 1

    minio_server_endpoint: str
    minio_root_user: str
    minio_root_password: str
    minio_server_secure: bool
    bucket_name: str = 'my-bucket'

    main_server_url: HttpUrl


config = Config()
