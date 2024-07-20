from minio import Minio

from minio_microservice.micro_config import config


def get_minio_client() -> Minio:
    return Minio(
        config.minio_server_endpoint,
        access_key=config.minio_root_user,
        secret_key=config.minio_root_password,
        secure=config.minio_server_secure,
    )
