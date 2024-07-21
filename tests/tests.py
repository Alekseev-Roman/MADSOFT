import pytest
import requests


@pytest.mark.parametrize('text', ['a very interesting joke', 'not bad meme text'])
@pytest.mark.parametrize('image_file', ['meme_img_1.jpeg', 'meme_img_2.jpeg'])
def test_post(text, image_file):
    res = requests.post(
        f'http://127.0.0.1:8080/memes?text={text}',
        files={'img_meme': open(f'./img/{image_file}', 'rb')}
    )
    assert res.json()['ok'] is True


@pytest.mark.parametrize('text', ['text_1', 'text_2'])
@pytest.mark.parametrize('image_file', ['meme_img_1.jpeg', 'meme_img_2.jpeg'])
def test_get_one(text, image_file):
    img = open(f'./img/{image_file}', 'rb')
    res_post = requests.post(
        f'http://127.0.0.1:8080/memes?text={text}',
        files={'img_meme': img}
    )
    res_get = requests.get(
        f'http://127.0.0.1:8080/memes?meme_id={res_post.json()["id"]}',
    )
    assert res_get.json()[0]['text'] == text
    img.seek(0)
    assert res_get.json()[0]['image'] == str(img.read())


@pytest.mark.parametrize('text', ['a very interesting joke', 'not bad meme text'])
@pytest.mark.parametrize('new_text', ['very new text', 'something very funny'])
@pytest.mark.parametrize('image_file', ['meme_img_1.jpeg', 'meme_img_2.jpeg'])
@pytest.mark.parametrize('new_image_file', ['meme_img_2.jpeg', 'meme_img_2.jpeg'])
def test_put(text, new_text, image_file, new_image_file):
    img = open(f'./img/{image_file}', 'rb')
    new_img = open(f'./img/{new_image_file}', 'rb')
    res_post = requests.post(
        f'http://127.0.0.1:8080/memes?text={text}',
        files={'img_meme': img}
    )

    res_put = requests.put(
        f'http://127.0.0.1:8080/memes?id={res_post.json()["id"]}&text={new_text}',
        files={'img_meme': new_img}
    )
    assert res_put.json()['ok'] is True

    res_get = requests.get(
        f'http://127.0.0.1:8080/memes?meme_id={res_post.json()["id"]}'
    )
    assert res_get.json()[0]['text'] == new_text
    new_img.seek(0)
    assert res_get.json()[0]['image'] == str(new_img.read())


@pytest.mark.parametrize('text', ['a very interesting joke', 'not bad meme text'])
@pytest.mark.parametrize('image_file', ['meme_img_1.jpeg', 'meme_img_2.jpeg'])
def test_delete(text, image_file):
    res_post = requests.post(
        f'http://127.0.0.1:8080/memes?text={text}',
        files={'img_meme': open(f'./img/{image_file}', 'rb')}
    )

    res_del = requests.delete(
        f'http://127.0.0.1:8080/memes?meme_id={res_post.json()["id"]}'
    )
    assert res_del.json()['ok'] is True

    res_get = requests.get(
        f'http://127.0.0.1:8080/memes?meme_id={res_post.json()["id"]}'
    )
    assert res_get.json() == []


