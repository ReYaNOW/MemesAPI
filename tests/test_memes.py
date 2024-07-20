import io

from conftest import IMG_PATH, async_session_maker_test, client
from PIL import Image, ImageChops
from sqlalchemy import select

from memesapi.memes.models import Memes


async def get_meme_from_db():
    async with async_session_maker_test() as session:
        query = select(Memes)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def test_add_meme():
    with open(f'{IMG_PATH}img_for_test.jpg', 'rb') as file:
        response = client.post(
            '/memes', data={'text': 'Some funny stuff'}, files={'image': file}
        )

    assert response.status_code == 201

    async with async_session_maker_test() as session:
        query = select(Memes)
        result = await session.execute(query)

        memes = result.scalars().all()

    meme = memes[0]
    assert meme is not None, 'Meme was not added to the DB'
    assert meme.id == 1
    assert meme.text == 'Some funny stuff'
    assert (
        'test.jpg' in meme.image_name
    ), 'Meme was saved with the wrong image_name'
    assert (
        meme.image_name != 'test.jpg'
    ), 'Meme was saved without a unique identifier'

    assert len(memes) == 1, 'Several memes was added instead of one'

    response = client.get('/memes/1/image')
    assert response.status_code == 200

    orig_img = Image.open(f'{IMG_PATH}img_for_test.jpg')
    img_from_response = Image.open(io.BytesIO(response.content))
    diff = ImageChops.difference(orig_img, img_from_response)

    assert diff.getbbox() is None, 'Images are not same'


def test_negative_add_meme():
    with open(f'{IMG_PATH}img_for_test.jpg', 'rb') as file:
        response = client.post('/memes', files={'image': file})

    assert (
        response.status_code == 422
    ), 'No HTTP 422 when trying to create without image'

    response = client.post('/memes', data={'text': 'Some funny stuff'})

    assert (
        response.status_code == 422
    ), 'No HTTP 422 when trying to create without text'


async def test_get_meme(add_meme):
    response = client.get('/memes/1')

    assert response.status_code == 200

    meme = await get_meme_from_db()

    meme_dict = response.json()
    correct_meme = {
        'id': meme.id,
        'image_name': meme.image_name.split('_', maxsplit=1)[1],
        'text': meme.text,
        'created_at': meme.created_at.isoformat(),
        'image_link': f'http://127.0.0.1:8000/memes/{meme.id}/image',
    }

    assert (
        meme_dict == correct_meme
    ), 'Wrong meme was received or with incomplete data'


async def test_get_list_of_memes(add_three_memes_and_get_data):
    response = client.get('/memes')
    assert response.json() == add_three_memes_and_get_data


async def test_update_meme(add_meme):
    with open(f'{IMG_PATH}img_for_test2.jpg', 'rb') as file:
        response = client.put(
            '/memes/1',
            data={'text': 'other funny stuff'},
            files={'image': file},
        )
        assert response.status_code == 200

        meme = await get_meme_from_db()

        assert meme.text == 'other funny stuff', 'Text of meme was not updated'

        img_response = client.get('/memes/1/image')
        orig_img = Image.open(f'{IMG_PATH}img_for_test2.jpg')
        img_from_response = Image.open(io.BytesIO(img_response.content))
        diff = ImageChops.difference(orig_img, img_from_response)

        assert diff.getbbox() is None, 'Image was not updated to the new one'


async def test_update_meme_only_text(add_meme):
    response = client.put('/memes/1', data={'text': 'other funny stuff'})
    assert response.status_code == 200

    meme = await get_meme_from_db()

    assert meme.text == 'other funny stuff', 'Text of meme was not updated'


async def test_delete_meme(add_meme):
    response = client.delete('/memes/1')
    assert response.status_code == 204

    meme = await get_meme_from_db()

    assert meme is None, 'Meme was not deleted'
