import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from models.base import Base
from models.user import User
from models.thread import Thread
from models.message import Message


config = context.config
DATABASE_URL = config.get_main_option("sqlalchemy.url")

engine = create_async_engine(DATABASE_URL)


async def run_migrations_online():
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()


asyncio.run(run_migrations_online())
