from contextlib import asynccontextmanager
from functools import wraps
from os import environ

from fastapi import Request
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import sqlalchemy.ext.declarative as dec
from sqlalchemy.orm import sessionmaker
from data.config import *

SqlAlchemyBase = dec.declarative_base()

env = environ.get

__factory = None


def get_database_url(alembic: bool = False) -> str:
    schema = "postgresql+asyncpg"

    if alembic:
        schema = "postgresql"

    return (f"{schema}://{env('db_login')}:{env('db_password')}@"
            f"{env('db_host')}:{env('db_port')}/{env('db_name')}")


async def global_init():
    global __factory

    if __factory:
        return
    conn_str = get_database_url()

    engine = create_async_engine(conn_str, pool_pre_ping=True)

    async with engine.begin() as conn:
        # await conn.run_sync(SqlAlchemyBase.metadata.drop_all)
        await conn.run_sync(SqlAlchemyBase.metadata.create_all)

    __factory = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    from . import __all_models  # noqa


def create_session() -> AsyncSession:
    global __factory
    return __factory() # noqa


def get_session(request: Request):
    return request.state.session


def session_db(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with create_session() as session:
            return await func(*args, session=session, **kwargs)
    return wrapper
