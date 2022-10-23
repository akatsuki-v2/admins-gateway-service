from __future__ import annotations

from datetime import datetime

from . import BaseModel
from . import Status

# NOTE: the `country` field is iso-3166-1 alpha-2


class SignupForm(BaseModel):
    username: str
    password: str
    email_address: str
    country: str


class Account(BaseModel):
    account_id: int
    username: str
    email_address: str
    country: str
    created_at: datetime
    updated_at: datetime
    status: Status


class AccountUpdate(BaseModel):
    username: str | None
    email_address: str | None
    country: str | None  # iso-3166-1 alpha-2
