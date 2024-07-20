import asyncio
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from memesapi.database import get_async_session
from memesapi.memes.db_requests import (
    add_meme_to_db,
    delete_meme_from_db,
    get_img_name_from_db,
    get_meme_from_db,
    get_memes_from_db,
    update_meme_in_db,
)
from memesapi.memes.dependencies import (
    get_httpx_client,
    validate_img,
    validate_img_if_received,
)
from memesapi.memes.schemas import MemeCreate, MemeRead, Pagination
from memesapi.memes.service import (
    delete_image_from_minio,
    image_stream,
    send_img_to_minio_api,
)

router = APIRouter(
    prefix='/memes',
    tags=['Memes'],
)


@router.get('', response_model=list[MemeRead])
async def get_list_of_memes(
    pagination: Pagination = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    return await get_memes_from_db(session, pagination)


@router.get('/{id}', response_model=MemeRead)
async def get_meme(
    id: int, session: AsyncSession = Depends(get_async_session)
):
    return await get_meme_from_db(session, id)


@router.get('/{id}/image')
async def get_img_for_meme(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    img_name = await get_img_name_from_db(session, id)
    return StreamingResponse(image_stream(img_name))


@router.post(
    '', status_code=status.HTTP_201_CREATED, response_model=MemeCreate
)
async def add_meme(
    text: str = Form(...),
    image: UploadFile = Depends(validate_img),
    session: AsyncSession = Depends(get_async_session),
    httpx_client: httpx.AsyncClient = Depends(get_httpx_client),
):
    img_name = await send_img_to_minio_api(image, httpx_client)
    return await add_meme_to_db(session, img_name, text)


@router.put('/{id}', response_model=MemeCreate)
async def update_meme(
    id: int,
    text: Optional[str] = Form(None),
    image: UploadFile | None = Depends(validate_img_if_received),
    session: AsyncSession = Depends(get_async_session),
    httpx_client: httpx.AsyncClient = Depends(get_httpx_client),
):
    if not text and not image:
        raise HTTPException(
            status_code=400, detail='Either text or image must be provided'
        )

    new_values = {}

    if image:
        image_name = await get_img_name_from_db(session, id)
        _, new_values['image_name'] = await asyncio.gather(
            delete_image_from_minio(image_name, httpx_client),
            send_img_to_minio_api(image, httpx_client),
        )

    if text:
        new_values['text'] = text

    return await update_meme_in_db(session, id, new_values)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_meme(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    httpx_client: httpx.AsyncClient = Depends(get_httpx_client),
):
    image_name = await get_img_name_from_db(session, id)

    await delete_image_from_minio(image_name, httpx_client)
    await delete_meme_from_db(session, id)
