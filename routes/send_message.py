from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import APIRouter, Request, Depends

from config.logger import logger
from config.database import get_db
from config.rate_limiter import limiter
from utils.helper import ResponseHelper
from decorators.auth import api_key_required
from tasks import send_message_to_group, send_message_to_private

from models.user import TelegramUser

router = APIRouter()
response = ResponseHelper()


class GroupMessageBody(BaseModel):
    bot_token: str = Field(...,)
    group_id: str = Field(...,)
    thread_id: str = Field(None,)
    message: str = Field(...,)
    image_url: str = Field(None,)
    file_path: str = Field(None,)


@router.post("/send-message-group")
@limiter.limit("20/minute")
@api_key_required
async def send_message_group(request: Request, data: GroupMessageBody, db: Session = Depends(get_db)):
    task = send_message_to_group.apply_async(
        args=(data.bot_token, data.group_id,
              data.thread_id, data.message, data.image_url, data.file_path)
    )
    return response.success_response(200, "success", data={"task_id": task.id})


class PrivateMessageBody(BaseModel):
    bot_token: str = Field(...,)
    chat_id: str = Field(None,)
    mobile: str = Field(None,)
    message: str = Field(...,)
    image_url: str = Field(None,)
    file_path: str = Field(None,)


@router.post("/send-message-private")
@limiter.limit("20/minute")
@api_key_required
async def send_message_private(request: Request, data: PrivateMessageBody, db: Session = Depends(get_db)):
    if not data.chat_id and not data.mobile:
        logger.error(
            "Either chat_id or mobile number must be provided")
        return response.error_response(400, "Either chat_id or mobile number must be provided")

    if data.chat_id:
        task = send_message_to_private.apply_async(
            args=(data.bot_token, data.chat_id, data.message,
                  data.image_url, data.file_path)
        )
        return response.success_response(200, "success", data={"task_id": task.id})

    db_user = db.query(TelegramUser).filter(
        TelegramUser.mobile == data.mobile).first()
    if not db_user:
        logger.error(
            f"User not found with: {data.mobile}")
        return response.error_response(404, "User not found")

    task = send_message_to_private.apply_async(
        args=(data.bot_token, db_user.chat_id,
              data.message, data.image_url, data.file_path)
    )
    return response.success_response(200, "success", data={"task_id": task.id})
