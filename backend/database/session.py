from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine

from backend.config import get_settings


settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
    _ensure_user_auth_columns()


def _ensure_user_auth_columns() -> None:
    statements = [
        "ALTER TABLE \"user\" ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255) NOT NULL DEFAULT ''",
        "ALTER TABLE \"user\" ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMP WITH TIME ZONE NULL",
    ]
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


def get_session():
    with Session(engine) as session:
        yield session
