from app.core.session import async_session


async def get_db():
    """
    Функция для создания асинхронной сессии

    :return:
    """

    try:
        async with async_session() as session:
            yield session
    finally:
        await session.close()