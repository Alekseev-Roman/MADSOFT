from fastapi import APIRouter, Depends, UploadFile, File, Response, HTTPException, status
from typing import Annotated
import requests

from schemas import MemeSchema, MemeSchemaAdd, MemeSchemaResult, MemeSchemaGet
from meme_db import MemeDB


router = APIRouter()


@router.get(path='/memes')
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


@router.get(path='/image')
async def get_meme(meme_id: int):
    memes = await MemeDB.find_one(meme_id)

    if memes[0]:
        img = requests.get(f'http://private_api:8088/images/memes?meme_id={meme_id}')
        return Response(content=img.content, media_type="image/jpg")
    else:
        raise HTTPException(detail="Meme not found.", status_code=status.HTTP_404_NOT_FOUND)


@router.post('/memes')
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


@router.put('/memes')
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


@router.delete('/memes')
async def delete_meme(meme_id: int) -> MemeSchemaResult:
    res = await MemeDB.delete_one(meme_id)
    requests.delete(f'http://private_api:8088/images/memes?meme_id={meme_id}&bucket_name={"madsoft-test-task"}')
    return {'ok': res[0], 'id': res[1], 'result': res[2]}
