import httpx
from fastapi import File, HTTPException, UploadFile


async def validate_img(image: UploadFile):
    if not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=415,
            detail='Only images are allowed',
        )

    return image


async def validate_img_if_received(image: UploadFile = File(None)):
    if image:
        return await validate_img(image)


async def get_httpx_client() -> httpx.AsyncClient:
    async with httpx.AsyncClient(timeout=None) as client:
        yield client
