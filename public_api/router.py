from fastapi import APIRouter, Depends, UploadFile, File, Response, HTTPException, status
from typing import Annotated
import requests

from schemas import MemeSchema, MemeSchemaAdd, MemeSchemaResult, MemeSchemaGet
from meme_db import MemeDB


router = APIRouter()


@router.get(path='/memes', description='''
Получение одного или нескольких мемов:
1. Для получение конкретного мема укажите meme_id.
2. Для получения нескольких мемов укажите page_number, а meme_id оставьте пустым.

При указании page_number будут возвращены от 0 до 10 мемов, которые находятся на соответствующей странице.

В случае, если указаны оба аргумента, будет возвращен мем с указанным meme_id. 

В случае, когда не указан ни один аргумент, будет возвращена страница с первыми 10 мемами.

Запрос возвращет список с мемами в виде объектов с текстом и байт строками изображений, который может содержать 
от 0 до 10 мемов, в зависимости от аргументов и количества подходящих мемов в БД.
''')
async def get_meme(meme_id: int = None, page_number: int = 0) -> list[MemeSchemaGet]:
    if meme_id is None:
        res, meme_texts = await MemeDB.find_all(0 if page_number < 0 else page_number)
    else:
        res, meme_texts = await MemeDB.find_one(meme_id)

    if res:
        memes = []
        for meme in meme_texts:
            img = requests.get(f'http://private_api:8088/images/memes?meme_id={meme.id}')
            memes.append(
                MemeSchemaGet(text=meme.text, image=str(img.content), id=meme.id)
            )
        return memes
    else:
        raise HTTPException(detail="Meme not found.", status_code=status.HTTP_404_NOT_FOUND)


@router.get(path='/image', description='''
Получение изображения мема для user-friendly взаимодейтсвия, т.к. GET запрос /memes возвращает строку байтов для 
изобаржения.

Запрос принимает аргумент meme_id - id мема.

Запрос возвращает изображение мема.
''')
async def get_meme(meme_id: int):
    memes = await MemeDB.find_one(meme_id)

    if memes[0]:
        img = requests.get(f'http://private_api:8088/images/memes?meme_id={meme_id}')
        return Response(content=img.content, media_type="image/jpg")
    else:
        raise HTTPException(detail="Meme not found.", status_code=status.HTTP_404_NOT_FOUND)


@router.post('/memes', description='''
Добавление нового мема.

Запрос принимает text - текст мема, и img_meme - изображение мема.

Запрос возвращает объект с полями: ok - флаг успеха, id - присвоенный мему id, result - строка с описание результата.
''')
async def post_meme(
        img_meme: Annotated[UploadFile, File(description='An image file of your meme', media_type='image/jpeg')],
        text_meme: Annotated[MemeSchemaAdd, Depends()]
) -> MemeSchemaResult:
    res = await MemeDB.add_one(text_meme)
    requests.post(
        f'http://private_api:8088/images/memes?meme_id={res[1]}&bucket_name={"madsoft-test-task"}',
        files={'img_meme': img_meme.file}
    )
    return {'ok': res[0], 'id': res[1], 'result': res[2]}


@router.put('/memes', description='''
Обновление мема.

Запрос принимает id - id изменяемого мема, text - новый текст для мема, img_meme - новое изображение для мема.

Запрос возвращает объект с полями: ok - флаг успеха, id - присвоенный мему id, result - строка с описание результата.
''')
async def put_meme(
        meme: Annotated[MemeSchema, Depends()],
        img_meme: Annotated[UploadFile, File(description='An image file of your meme', media_type='image/jpeg')],
) -> MemeSchemaResult:
    res = await MemeDB.update_one(MemeSchema(id=meme.id, text=meme.text))
    requests.put(
        f'http://private_api:8088/images/memes?meme_id={meme.id}&bucket_name={"madsoft-test-task"}',
        files={'img_meme': img_meme.file}
    )
    return {'ok': res[0], 'id': res[1], 'result': res[2]}


@router.delete('/memes', description='''
Удаление мема.

Запрос принимает id - id удаляемого мема.

Запрос возвращает объект с полями: ok - флаг успеха, id - присвоенный мему id, result - строка с описание результата.
''')
async def delete_meme(meme_id: int) -> MemeSchemaResult:
    res = await MemeDB.delete_one(meme_id)
    requests.delete(f'http://private_api:8088/images/memes?meme_id={meme_id}&bucket_name={"madsoft-test-task"}')
    return {'ok': res[0], 'id': res[1], 'result': res[2]}
