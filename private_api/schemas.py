from pydantic import BaseModel
from fastapi import APIRouter, Depends, UploadFile, File


class MemeSchemaS3Params(BaseModel):
    meme_id: int
    bucket_name: str
    object_name: str


class MemeSchemaS3(MemeSchemaS3Params):
    img: bytes


class MemeSchemaS3Result(BaseModel):
    ok: bool = True
    object_name: str
    result: str


class MemeSchemaS3GetResult(MemeSchemaS3Result):
    img: bytes
