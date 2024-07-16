from fastapi import APIRouter, Response, Request

from schemas import MemeSchemaS3, MemeSchemaS3Result, MemeSchemaS3Params
from meme_db import MemeDB


router = APIRouter(prefix='/images')


@router.get(
    path='/memes',
    responses={
        200: {
            "content": {"image/jpg": {}}
        }
    },
    response_class=Response
)
async def get_meme(meme_id: int, object_name: str = None, bucket_name: str = 'madsoft-test-task'):
    if object_name is None:
        img = await MemeDB.find_one(bucket_name, f'{bucket_name}_{meme_id}')
    else:
        img = await MemeDB.find_one(bucket_name, object_name)
    return Response(content=img[3], media_type="image/jpg")


@router.post('/memes')
async def post_meme(
        meme_id: int,
        req: Request,
        object_name: str = None,
        bucket_name: str = 'madsoft-test-task'
) -> MemeSchemaS3Result:
    data = await req.form()
    img = await data.get('img_meme').read()
    object_name = object_name if object_name else f'{bucket_name}_{meme_id}'
    res = await MemeDB.add_one(
        MemeSchemaS3(
            meme_id=meme_id, img=img,
            object_name=object_name,
            bucket_name=bucket_name
        )
    )
    return {'ok': res[0], 'object_name': res[1], 'result': res[2]}


@router.put('/memes')
async def put_meme(
        meme_id: int,
        req: Request,
        object_name: str = None,
        bucket_name: str = 'madsoft-test-task'
) -> MemeSchemaS3Result:
    data = await req.form()
    img = await data.get('img_meme').read()
    object_name = object_name if object_name else f'{bucket_name}_{meme_id}'
    res = await MemeDB.update_one(
        MemeSchemaS3(
            meme_id=meme_id, img=img,
            object_name=object_name,
            bucket_name=bucket_name
        )
    )
    return {'ok': res[0], 'object_name': res[1], 'result': res[2]}


@router.delete('/memes')
async def delete_meme(
        meme_id: int,
        object_name: str = None,
        bucket_name: str = 'madsoft-test-task'
) -> MemeSchemaS3Result:
    object_name = object_name if object_name else f'{bucket_name}_{meme_id}'
    res = await MemeDB.delete_one(
        MemeSchemaS3Params(
            meme_id=meme_id,
            object_name=object_name,
            bucket_name=bucket_name
        )
    )
    return {'ok': res[0], 'object_name': res[1], 'result': res[2]}
