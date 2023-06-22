import uuid
from datetime import datetime

from pydantic import BaseModel


class Movie(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
