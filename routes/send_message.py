from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import APIRouter, Request, Depends

from config.logger import logger
from config.database import get_db
from utils.helper import ResponseHelper
from decorators.auth import api_key_required
from tasks import send_message_to_group, send_message_to_private

from models.user import TelegramUser

router = APIRouter()
response = ResponseHelper()


class GroupMessageBody(BaseModel):
    api_token: str = Field(...,)
    group_id: str = Field(...,)
    thread_id: str = Field(None,)
    message: str = Field(...,)
    image_url: str = Field(None,)
    file_path: str = Field(None,)


@router.post("/send-message-group")
@api_key_required
async def send_message_group(request: Request, data: GroupMessageBody, db: Session = Depends(get_db)):
    task = send_message_to_group.apply_async(
        args=(data.api_token, data.group_id,
              data.thread_id, data.message, data.image_url, data.file_path)
    )
    return response.success_response(200, "success", data={"task_id": task.id})


class PrivateMessageBody(BaseModel):
    mobile: str = Field(...,)
    message: str = Field(...,)
    image_url: str = Field(None,)
    file_path: str = Field(None,)


@router.post("/send-message-private")
@api_key_required
async def send_message_private(request: Request, data: PrivateMessageBody, db: Session = Depends(get_db)):
    db_user = db.query(TelegramUser).filter(
        TelegramUser.mobile == data.mobile).first()
    if not db_user:
        logger.error(
            f"User not found with: {data.mobile}")
        return response.error_response(404, "User not found")

    task = send_message_to_private.apply_async(
        args=(db_user.chat_id, data.message, data.image_url, data.file_path)
    )
    return response.success_response(200, "success", data={"task_id": task.id})
