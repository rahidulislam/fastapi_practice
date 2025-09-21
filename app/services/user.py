from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.utils import generate_access_token
from app.database.models import User
from .base import BaseService

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UserService(BaseService):
    def __init__(self, model:User, session:AsyncSession):
        self.model=model
        self.session=session

    async def _add_user(self, data:dict):
        user = self.model(
            **data,
            password_hash=password_context.hash(data["password"])
        )
        return await self._add(user)

    async def _get_by_email(self, email)->User|None:
        return await self.session.scalar(
            select(self.model).where(self.model.email==email)
        )
    
    async def _generate_token(self, email,password):
        user = await self._get_by_email(email)
        
        if user is None or not password_context.verify(
            password, user.password_hash
        ):
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or Password is incorrect",
            )
        return generate_access_token(
            data={
                "user": {
                    "id": str(user.id),
                    "name": user.name,
                    "email": user.email,
                }
            }
        )
