import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context

from app.core.config import settings
from app.db.models import Base


# ------------------------
# Alembic конфиги
# ------------------------

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata
DATABASE_URL = settings.db_url
print(Base.metadata.schema)

# ------------------------
# Offline mode
# ------------------------

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# ------------------------
# Online mode (async)
# ------------------------

def run_migrations_online():
    """Run migrations in 'online' mode using async engine."""

    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async def do_run_migrations():
        async with connectable.connect() as async_connection:
            def sync_run_migrations(sync_connection):
                context.configure(
                    connection=sync_connection,
                    target_metadata=target_metadata,
                    compare_type=True,
                    render_as_batch=True,
                    version_table_schema=settings.POSTGRES_SCHEMA
                )
                with context.begin_transaction():
                    context.run_migrations()

            await async_connection.run_sync(sync_run_migrations)

    asyncio.run(do_run_migrations())

# ------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
