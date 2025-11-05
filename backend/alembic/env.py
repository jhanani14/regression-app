import os
import sys
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# ------------------------------
# Add project root to sys.path
# ------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(ROOT_DIR)

# ------------------------------
# Load .env from project root
# ------------------------------
load_dotenv(os.path.join(ROOT_DIR, ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

# ------------------------------
# Alembic Config object
# ------------------------------
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# ------------------------------
# Logging
# ------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ------------------------------
# Import Base for autogenerate
# ------------------------------
from app.db.base import Base  # Base must include all models
target_metadata = Base.metadata

# ------------------------------
# Offline migration
# ------------------------------
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# ------------------------------
# Online migration
# ------------------------------
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True  # optional, detects column type changes
        )
        with context.begin_transaction():
            context.run_migrations()

# ------------------------------
# Run migrations based on mode
# ------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
