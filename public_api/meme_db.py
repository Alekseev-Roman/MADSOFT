from sqlalchemy import select, update, delete

from sql_database import new_session, MemeTextModel
from schemas import MemeSchema, MemeSchemaAdd


class MemeDB:
    @classmethod
    async def find_all(cls, page_number: int):
        try:
            async with new_session() as session:
                query = select(MemeTextModel)
                res = await session.execute(query)
                task_models = res.scalars().all()
                return True, task_models[10 * (page_number + 1):10 * (page_number + 1) + 10]
        except Exception as e:
            return False, []

    @classmethod
    async def find_one(cls, meme_id: int):
        try:
            async with new_session() as session:
                query = select(MemeTextModel).where(MemeTextModel.id == meme_id)
                res = await session.execute(query)
                task_model = res.scalars().all()
                return True, task_model
        except Exception as e:
            return False, []

    @classmethod
    async def add_one(cls, new_meme: MemeSchemaAdd):
        try:
            async with new_session() as session:
                meme_dict = new_meme.model_dump()
                meme = MemeTextModel(**meme_dict)
                session.add(meme)
                await session.flush()
                await session.commit()
                return True, meme.id, 'Success'
        except Exception as e:
            return False, -1, f'Entry was not added.'

    @classmethod
    async def delete_one(cls, meme_id: int):
        try:
            async with new_session() as session:
                query = (
                    delete(MemeTextModel)
                    .where(MemeTextModel.id == meme_id)
                )
                res = await session.execute(query)
                await session.flush()
                await session.commit()
                if res.rowcount == 1:
                    return True, meme_id, 'Success'
                else:
                    return False, meme_id, f'Entry by id: {meme_id} was not deleted'
        except Exception as e:
            return False, meme_id, f'Entry by id: {meme_id} was not deleted'

    @classmethod
    async def update_one(cls, updated_meme: MemeSchema):
        try:
            async with new_session() as session:
                query = (
                    update(MemeTextModel)
                    .where(MemeTextModel.id == updated_meme.id)
                    .values(text=updated_meme.text)
                )
                res = await session.execute(query)
                await session.flush()
                await session.commit()
                if res.rowcount == 1:
                    return True, updated_meme.id, 'Success'
                else:
                    return False, updated_meme.id, f'Entry by id: {updated_meme.id} was not updated'
        except Exception as e:
            return False, updated_meme.id, f'Entry by id: {updated_meme.id} was not updated'
