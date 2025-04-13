import enum
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.dialects.postgresql import TIMESTAMP, ENUM
from sqlalchemy.orm import  Mapped, mapped_column, DeclarativeBase, declared_attr

load_dotenv()

class DB:
    DB_USER = os.getenv('DB_USER')
    DB_PORT = os.getenv('DB_PORT')
    DB_HOST = os.getenv('DB_HOST')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


SQLALCHEMY_DATABASE_URL = DB.URL

engine = create_async_engine(DB.URL, echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class UserRole(enum.Enum):
    ADMIN = "admin"
    PATIENT = "patient"
    DOCTOR = "doctor"


# BASE MODEL

class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'


class CreatedModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))

# Other Models

class User(CreatedModel):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String(50), nullable=False)
    hashed_password = Column(String)
    role = Column(
        ENUM(UserRole, name="user_role_enum", create_type=False, native_enum=True,
             values_callable=lambda obj: [e.value for e in obj]),
        default=UserRole.PATIENT,
        nullable=False
    )


async def init_db():
    async with engine.begin() as conn:
        # Create the ENUM type if it does not exist
        user_role_enum = Enum(UserRole, name="user_role_enum")
        await conn.run_sync(lambda sync_conn: user_role_enum.create(bind=sync_conn, checkfirst=True))
        # Create tables after the enum type is created
        await conn.run_sync(Base.metadata.create_all)