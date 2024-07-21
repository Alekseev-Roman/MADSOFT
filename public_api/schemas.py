from pydantic import BaseModel


class MemeSchemaAdd(BaseModel):
    text: str


class MemeSchema(MemeSchemaAdd):
    id: int


class MemeSchemaResult(BaseModel):
    ok: bool = True
    id: int
    result: str


class MemeSchemaGet(MemeSchema):
    image: str
