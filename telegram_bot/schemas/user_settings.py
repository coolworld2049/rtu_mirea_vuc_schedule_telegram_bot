from datetime import datetime

from pydantic import BaseModel


class UserSettingsBase(BaseModel):
    platoon: int | None = None
    course: int | None = None


class UserSettings(UserSettingsBase):
    user_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
