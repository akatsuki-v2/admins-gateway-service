from __future__ import annotations

from datetime import datetime
from uuid import UUID

from . import BaseModel


class LoginForm(BaseModel):
    identifier: str
    passphrase: str
    user_agent: str  # TODO: literal?


class Session(BaseModel):
    session_id: UUID
    account_id: int
    user_agent: str
    expires_at: datetime
    created_at: datetime
    updated_at: datetime

# class SessionUpdate(BaseModel):
#     expires_at: datetime | None
