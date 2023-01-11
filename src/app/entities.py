from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class AbstractEntity(BaseModel):
    id: Optional[int]


class TodoEntry(AbstractEntity):
    summary: str
    detail: Optional[str]
    tags: Optional[List[str]] = []
    created_at: datetime
