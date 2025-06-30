import json
from datetime import datetime
from enum import Enum
from typing import List, Optional, Any

from pydantic import BaseModel, validator


class NotificationEngine(str, Enum):
    telegram = "telegram"
    email = "email"
    sms = "sms"


class NotificationStatus(str, Enum):
    pending = "pending"
    canceled = "canceled"
    failed = "failed"
    sent = "sent"


class NotificationType(str, Enum):
    payment = "payment"
    order = "order"
    transaction = "transaction"
    general = "general"
    account = "account"
    used_traffic = "used_traffic"
    expire_time = "expire_time"


class NotificationUsedTrafficLevel(int, Enum):
    fifty_percent = 50
    eighty_percent = 80
    ninety_five_percent = 95
    full_percent_used = 100


class NotificationExpireTimeLevel(int, Enum):
    thirty_day = 1
    seven_day = 2
    three_day = 3
    one_day = 4
    expired = 5


class NotificationBase(BaseModel):
    user_id: int
    account_id: Optional[int] = None
    level: int
    message: str = None
    details: str = None
    keyboard: Optional[Any] = None
    photo_url: Optional[str] = None

    approve: bool = False
    send_to_admin: Optional[bool] = False

    engine: Optional[NotificationEngine] = NotificationEngine.telegram
    status: Optional[NotificationStatus] = NotificationStatus.pending
    type: NotificationType

    @validator("keyboard", pre=True, always=True)
    def validate_keyboard_json(cls, v):
        if v is None:
            return v
        if isinstance(v, (dict, list)):
            return v
        if isinstance(v, str):
            if not v.strip():
                return None
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("The keyboard field contains invalid JSON")
        raise ValueError("Keyboard must be a valid JSON string or object")


class NotificationCreate(NotificationBase):
    pass


class NotificationModify(NotificationBase):
    id: int


class NotificationResponse(NotificationBase):
    id: int
    account_id: Optional[int] = None
    user_id: Optional[int] = None

    created_at: datetime
    modified_at: datetime

    @validator("keyboard", pre=True, always=True)
    def serialize_keyboard_from_db(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return None  # Or handle as an error
        return v

    class Config:
        orm_mode = True


class NotificationsResponse(BaseModel):
    notifications: List[NotificationResponse]
    total: int
