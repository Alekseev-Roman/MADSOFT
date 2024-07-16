from s3_database import session
from schemas import MemeSchemaS3, MemeSchemaS3Params

import io


class MemeDB:
    @classmethod
    async def find_one(cls, bucket_name: str, object_name: str):
        try:
            obj = session.get_object(bucket_name, object_name)
            return True, object_name, f'Image {object_name} got from bucket: {bucket_name}', obj.data
        except Exception as e:
            return False, object_name, f"Image {object_name} didn't get from bucket: {bucket_name}", b""

    @classmethod
    async def add_one(cls, new_meme_s3: MemeSchemaS3):
        try:
            raw_img = io.BytesIO(new_meme_s3.img)
            session.put_object(new_meme_s3.bucket_name, new_meme_s3.object_name, raw_img, raw_img.getbuffer().nbytes)
            return (
                True,
                new_meme_s3.object_name,
                f'Image of meme with id: {new_meme_s3.meme_id} was added to S3 by name: {new_meme_s3.object_name}'
            )
        except Exception as e:
            return False, new_meme_s3.object_name, f'Image of meme with id: {new_meme_s3.meme_id} was not added to S3.'

    @classmethod
    async def delete_one(cls, meme_s3: MemeSchemaS3Params):
        try:
            session.remove_object(meme_s3.bucket_name, meme_s3.object_name)
            return (
                True,
                meme_s3.object_name,
                f'Image of meme with id: {meme_s3.meme_id} and name: {meme_s3.object_name} was deleted'
            )
        except Exception as e:
            return False, meme_s3.object_name, f'Image of meme with id: {meme_s3.meme_id} was not deleted'

    @classmethod
    async def update_one(cls, updated_meme: MemeSchemaS3):
        try:
            session.remove_object(updated_meme.bucket_name, updated_meme.object_name)
            raw_img = io.BytesIO(updated_meme.img)
            session.put_object(updated_meme.bucket_name, updated_meme.object_name, raw_img, raw_img.getbuffer().nbytes)
            return (
                False,
                updated_meme.object_name,
                f'Image of meme with id: {updated_meme.meme_id} and name: {updated_meme.object_name} was updated'
            )
        except Exception as e:
            return False, updated_meme.object_name, f'Image of meme with id: {updated_meme.meme_id} was not updated'
