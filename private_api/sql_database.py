from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Model(DeclarativeBase):
    pass


class MemeTextModel(Model):
    __tablename__ = 'text'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str | None]


engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost/meme_db")
new_session = async_sessionmaker(engine, expire_on_commit=False)



