import logging
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool

import models
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = models.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

postgres_user = 'postgres'
postgres_password = 'postgres'
if 'POSTGRES_USER' in os.environ:
    postgres_user = os.environ['POSTGRES_USER']
    logging.info("Postgres username found in environ")
if 'POSTGRES_PASSWORD' in os.environ:
    postgres_password = os.environ['POSTGRES_PASSWORD']
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@postgres:5432/trinibytes_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = SQLALCHEMY_DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

#  poetry run alembic revision --autogenerate -m "Changes to caribbeanjobspost table"
#  poetry run alembic upgrade head
