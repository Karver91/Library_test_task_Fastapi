from sqlalchemy import select

from app.auth.models import User
from app.utils.repository import SQLAlchemyRepository


class AuthRepository(SQLAlchemyRepository):
    model = User

    def __init__(self, session):
        self.session = session

    async def get_user_by_email(self, email: str):
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()
