from datetime import datetime, timezone

import pytest

from entities import TodoEntry
from persistence.mapper.errors import EntityNotFoundMapperError
from persistence.mapper.mongodb import MongoDBTodoEntryMapper

_memory_storage = {
    1: TodoEntry(id=1, summary="Lorem Ipsum", created_at=datetime.now(tz=timezone.utc))
}


@pytest.mark.asyncio
async def test_get_todo_entry() -> None:
    mapper = MongoDBTodoEntryMapper(db='test', fixture=_memory_storage, clean=True)
    entity = await mapper.get(identifier=1)
    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_todo_entry_not_found_error() -> None:
    mapper = MongoDBTodoEntryMapper(db='test', clean=True)
    with pytest.raises(EntityNotFoundMapperError):
        await mapper.get(identifier=42)


@pytest.mark.asyncio
async def test_create_todo_entry() -> None:
    mapper = MongoDBTodoEntryMapper(db='test', clean=True)

    data = TodoEntry(
        summary="Finish coding challenge",
        detail="You're running late",
        created_at=datetime.now(tz=timezone.utc),
    )

    entity = await mapper.create(entity=data)
    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_update_todo_entry_tags() -> None:
    mapper = MongoDBTodoEntryMapper(db='test', clean=True)

    data = TodoEntry(
        summary="Lorem Ipsum",
        detail=None,
        created_at=datetime.now(tz=timezone.utc),
    )

    entity = await mapper.create(entity=data)

    entity.tags = ["doc", "secret"]

    await mapper.update(entity=entity)
    entity = await mapper.get(identifier=entity.id)
    
    assert len(entity.tags) == 2