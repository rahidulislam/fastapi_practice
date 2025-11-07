from xml.dom.minidom import parseString
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from regex import E

from app.config import notification_settings
from app.utils import TEMPLATE_DIR


class NotificationService:
    def __init__(self, tasks: BackgroundTasks):
        self.tasks = tasks
        self.fastmail = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump(), TEMPLATE_FOLDER=TEMPLATE_DIR
            )
        )

    async def send_email(self, subject: str, recipients: list[EmailStr], body: str):
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                subject=subject,
                recipients=recipients,
                body=body,
                subtype=MessageType.plain,
            ),
        )

    async def send_templated_email(
        self,
        subject: str,
        recipients: list[EmailStr],
        context: dict,
        template_name: str,
    ):
        self.tasks.add_task(
            self.fastmail.send_message,
            message = MessageSchema(
                subject=subject,
                recipients=recipients,
                template_body=context,
                subtype=MessageType.html,
            ),
            template_name=template_name,  
        )
