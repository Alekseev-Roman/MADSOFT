from fastapi import APIRouter, Depends, UploadFile, File
from typing import Annotated

from schemas import MemeSchema, MemeSchemaAdd, MemeSchemaResult
from meme_db import MemeDB


router = APIRouter()


@router.get('/memes')
async def get_meme(meme_id: int = None) -> list[MemeSchema]:
    if meme_id is None:
        memes = await MemeDB.find_all()
    else:
        memes = await MemeDB.find_one(meme_id)

    if memes[0]:
        return memes[1]
    else:
        return memes[1]


@router.post('/memes')
async def post_meme(
        img_meme: Annotated[UploadFile, File(description='An image file of your meme', media_type='image/jpeg')],
        text_meme: Annotated[MemeSchemaAdd, Depends()]
) -> MemeSchemaResult:
    res = await MemeDB.add_one(text_meme)
    print(img_meme.filename)
    return {'ok': res[0], 'id': res[1], 'result': res[2]}


@router.put('/memes')
async def put_meme(updated_meme: Annotated[MemeSchema, Depends()]) -> MemeSchemaResult:
    res = await MemeDB.update_one(updated_meme)
    return {'ok': res[0], 'id': res[1], 'result': res[2]}


@router.delete('/memes')
async def delete_meme(meme_id: int) -> MemeSchemaResult:
    res = await MemeDB.delete_one(meme_id)
    return {'ok': res[0], 'id': res[1], 'result': res[2]}
