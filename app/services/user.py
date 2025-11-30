from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from fastapi import BackgroundTasks, HTTPException, status
from app.services.notification import NotificationService
from app.utils import generate_access_token, generate_url_safe_token
from app.database.models import User
from .base import BaseService
from app.config import app_settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UserService(BaseService):
    def __init__(self, model:User, session:AsyncSession, task:BackgroundTasks):
        self.model=model
        self.session=session
        self.notification_service=NotificationService(task)

    async def _add_user(self, data:dict):
        user = self.model(
            **data,
            password_hash=password_context.hash(data["password"])
        )
        user = await self._add(user)
        token = generate_url_safe_token({
            "email": user.email,
            "id": user.id,
        })
        self.notification_service.send_email_with_template({
            "recipients": [user.email],
            "subject": "Verify your email",
            "context":{
                "username": user.name,
                "verification_url": f"http://{app_settings.APP_DOMAIN}/user/verify?token={token}",
            },
            "template_name": "mail_email_verify.html",

        })
        return user

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
        if not user.email_verified:
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email is not verified",
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
