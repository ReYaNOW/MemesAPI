from datetime import datetime

import httpx
from fastapi import HTTPException, UploadFile

from memesapi.config import config


def get_unique_filename(filename: str):
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    unique_filename = f'{timestamp}_{filename}'

    return unique_filename


async def send_img_to_minio_api(image: UploadFile, client: httpx.AsyncClient):
    filename = get_unique_filename(image.filename)
    image_as_bytes = await image.read()

    response = await client.post(
        f'{config.private_server_url.unicode_string()}minio/upload',
        data={'filename': filename},
        files={'file': image_as_bytes},
    )
    if response.status_code != 201:
        raise HTTPException(status_code=500)

    return filename


async def delete_image_from_minio(filename: str, client: httpx.AsyncClient):
    response = await client.delete(
        f'{config.private_server_url.unicode_string()}minio/delete/{filename}',
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500)


async def image_stream(img_name: str):
    domain = config.private_server_url.unicode_string()
    url = f'{domain}minio/download/{img_name}'

    async with httpx.AsyncClient() as client:
        async with client.stream('GET', url) as r:
            async for chunk in r.aiter_bytes():
                yield chunk
