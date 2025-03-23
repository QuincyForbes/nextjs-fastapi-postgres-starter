"""
Alembic asynchronous migration script.

This script is used by Alembic to run database migrations in an asynchronous context,
leveraging SQLAlchemy's async engine. It sets up the connection and executes
schema migrations defined in Alembic's versions folder.

Usage:
    Typically invoked automatically by Alembic when using `alembic upgrade head`
    or other CLI commands with appropriate configuration.

Dependencies:
    - SQLAlchemy (async engine)
    - Alembic
"""

import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from models.base import Base

config = context.config
DATABASE_URL = config.get_main_option("sqlalchemy.url")

engine = create_async_engine(DATABASE_URL)


async def run_migrations_online():
    """
    Run database migrations in an asynchronous context.

    This function establishes an asynchronous connection using SQLAlchemy's async engine
    and delegates the migration process to `do_run_migrations`.
    """
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    """
    Configure Alembic's migration context and execute migrations.

    Args:
        connection: A SQLAlchemy connection object passed from the async context.

    This function binds the metadata and starts a transaction to apply migrations.
    """
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()


asyncio.run(run_migrations_online())
