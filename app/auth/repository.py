from sqlalchemy import Select, Insert, Update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User


class UserRepository:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session

    async def get_user_by_username(
            self,
            username
    ) -> User | None:
        stmt = Select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def get_user_by_email(
            self,
            email: str
    ) -> User:
        stmt = Select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def create_user(
            self,
            username: str,
            email: str,
            full_name: str,
            hashed_password: str,
            role: str = "client"
    ) -> User:
        stmt = Insert(User).values(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            role=role,
        ).returning(User)
        result = await self.session.execute(stmt)
        await self.session.flush()
        user = result.scalars().first()
        return user

    async def get_user_by_id(
            self,
            user_id: int
    ) -> User:
        stmt = Select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def udate_password(
            self,
            user_id: int,
            hashed_password: str
    ) -> None:
        stmt = Update(User).where(User.id == user_id).values(
            hashed_password=hashed_password,
        )
        await self.session.execute(stmt)
        await self.session.flush()
