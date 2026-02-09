from app.core.session import async_session


async def get_db():
    """
    Функция для создания асинхронной сессии
    
    """
    async with async_session() as session:
        yield session




