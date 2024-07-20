from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from minio_microservice.files.dependencies import get_minio_client
from minio_microservice.files.router import router as files_router
from minio_microservice.micro_config import config


@asynccontextmanager
async def lifespan(_):
    client = get_minio_client()

    if not client.bucket_exists(config.bucket_name):
        client.make_bucket(config.bucket_name)
        print('Created bucket', config.bucket_name)
    yield


app = FastAPI(title='MinIO Server API', lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.main_server_url],
    allow_methods=['GET', 'POST'],
    allow_headers=['*'],
)

app.include_router(files_router)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.host,
        port=config.private_server_url.port,
        workers=config.workers,
    )
