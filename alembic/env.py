import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import create_engine, pool

from alembic import context


# Add your project’s directory to the path so that Alembic can find your models.
sys.path.append(str(Path(__file__).resolve().parent.parent))


from database.db import Base, DB  # Import your Base class for models

DATABASE_URL = DB.URL

# Set the SQLAlchemy URL
config = context.config
config.set_main_option('sqlalchemy.url', DATABASE_URL)

# This is the Alembic Config object
fileConfig(config.config_file_name)

# Configure the target metadata for 'autogenerate' support
target_metadata = Base.metadata

# Function to run migrations online
def run_migrations_online():
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
