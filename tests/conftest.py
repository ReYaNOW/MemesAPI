from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import delete, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from memesapi.config import config
from memesapi.database import get_async_session
from memesapi.main import app
from memesapi.memes.models import Memes, metadata

test_db_url = config.database_url.unicode_string()

async_engine_test = create_async_engine(test_db_url, poolclass=NullPool)

async_session_maker_test = async_sessionmaker(
    async_engine_test, expire_on_commit=False
)

metadata.bind = async_engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker_test() as session:
        yield session


app.dependency_overrides[  # noqa
    get_async_session
] = override_get_async_session  # noqa


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with async_engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with async_engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(autouse=True, scope='function')
async def clear_db_and_reset_id_counter():
    stmt = delete(Memes)
    reset_sequence_stmt = 'ALTER SEQUENCE memes_id_seq RESTART WITH 1'
    async with async_session_maker_test() as session:
        await session.execute(stmt)
        await session.execute(text(reset_sequence_stmt))
        await session.commit()


client = TestClient(app)

IMG_PATH = 'tests/fixtures/meme_images/'


@pytest.fixture(scope='function')
def add_meme():
    with open(f'{IMG_PATH}img_for_test.jpg', 'rb') as file:
        client.post(
            '/memes', data={'text': 'Some funny stuff'}, files={'image': file}
        )


@pytest.fixture(scope='function')
def add_three_memes_and_get_data():
    response_contents = []
    for _ in range(3):
        with open(f'{IMG_PATH}img_for_test.jpg', 'rb') as file:
            resp1 = client.post(
                '/memes',
                data={'text': 'Some funny stuff'},
                files={'image': file},
            )
            resp2 = client.get(f'/memes/{resp1.json()["id"]}')
            response_contents.append(resp2.json())

    return response_contents


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(base_url='http://127.0.0.1:8000') as ac:
        yield ac
