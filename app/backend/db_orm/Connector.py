from backend.src.settings import settings
from sqlalchemy import String, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated


sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=bool(settings.GLOBAL_CONFIG["debug"]),
    pool_size=settings.GLOBAL_CONFIG["max_db_sess"],
    max_overflow=100,
)
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=bool(settings.GLOBAL_CONFIG["debug"]),
    pool_size=settings.GLOBAL_CONFIG["max_db_sess"],
    max_overflow=100,
)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
