from pydantic import BaseModel
from datetime import datetime


class UrlSchema(BaseModel):
    original_url: str
    expires_at : datetime | None = None
    is_active : bool = True


class UrlResponseSchema(BaseModel):
    id: int
    original_url: str
    short_code: str
    created_at: datetime
    expires_at: datetime | None
    is_active: bool
