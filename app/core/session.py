from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.settings import settings

engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
