from fastapi import HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from memesapi.memes.models import Memes
from memesapi.memes.schemas import Pagination


async def get_memes_from_db(session, pagination: Pagination):
    query = (
        select(Memes)
        .limit(pagination.limit)
        .offset(pagination.limit * pagination.page - pagination.limit)
        .order_by(pagination.order_by)
    )
    result = await session.execute(query)

    memes = result.scalars().all()

    return memes


async def add_meme_to_db(session, image_name, text):
    stmt = (
        insert(Memes)
        .values(image_name=image_name, text=text)
        .returning(Memes.__table__)
    )
    result = await session.execute(stmt)
    await session.commit()

    return result.first()


async def get_meme_from_db(session: AsyncSession, id: int):
    query = select(Memes).where(Memes.id == id)
    result = await session.execute(query)
    meme = result.scalar_one_or_none()

    if not meme:
        raise HTTPException(
            status_code=404,
            detail='Meme with such id is not found',
        )
    return meme


async def update_meme_in_db(session: AsyncSession, id, new_values):
    stmt = (
        update(Memes)
        .values(**new_values)
        .where(Memes.id == id)
        .returning(Memes.__table__)
    )
    result = await session.execute(stmt)
    await session.commit()

    return result.first()


async def get_img_name_from_db(session: AsyncSession, id):
    query = select(Memes.image_name).where(Memes.id == id)
    result = await session.execute(query)
    img_name = result.scalar()

    if not img_name:
        raise HTTPException(
            status_code=404,
            detail='Image for a meme with such id is not found',
        )

    return img_name


async def delete_meme_from_db(session: AsyncSession, id):
    stmt = delete(Memes).where(Memes.id == id)
    await session.execute(stmt)
    await session.commit()
