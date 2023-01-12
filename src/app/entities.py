from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class AbstractEntity(BaseModel):
    id: Optional[int]

    @classmethod
    def from_db(cls, **data):
        id = data.pop('_id')
        return cls(id=id, **data)

    def to_db(self):
        data = dict(self).copy()
        data['_id'] = data.pop('id')
        return data


class TodoEntry(AbstractEntity):
    summary: str
    detail: Optional[str]
    tags: Optional[List[str]] = []
    created_at: datetime
