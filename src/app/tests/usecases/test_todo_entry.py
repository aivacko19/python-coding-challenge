from datetime import datetime, timezone
from xml.dom.minidom import Identified

import pytest

from entities import TodoEntry
from persistence.mapper.memory import MemoryTodoEntryMapper
from persistence.repository import TodoEntryRepository
from usecases import get_todo_entry, NotFoundError, create_todo_entry, UseCaseError, add_tags_to_todo_entry

_storage = {
    1: TodoEntry(id=1, summary="Lorem Ipsum", created_at=datetime.now(tz=timezone.utc))
}


@pytest.mark.asyncio
async def test_get_todo_entry() -> None:
    mapper = MemoryTodoEntryMapper(storage=_storage)
    repository = TodoEntryRepository(mapper=mapper)

    entity = await get_todo_entry(identifier=1, repository=repository)

    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_get_not_existing_todo_entry() -> None:
    mapper = MemoryTodoEntryMapper(storage=_storage)
    repository = TodoEntryRepository(mapper=mapper)

    with pytest.raises(NotFoundError):
        await get_todo_entry(identifier=42, repository=repository)


@pytest.mark.asyncio
async def test_create_todo_entry() -> None:
    mapper = MemoryTodoEntryMapper(storage=_storage)
    repository = TodoEntryRepository(mapper=mapper)

    data = TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc))
    entity = await create_todo_entry(entity=data, repository=repository)

    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_todo_entry_creation_error() -> None:
    mapper = MemoryTodoEntryMapper(storage=None)
    repository = TodoEntryRepository(mapper=mapper)

    data = TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc))
    with pytest.raises(UseCaseError):
        await create_todo_entry(entity=data, repository=repository)


@pytest.mark.asyncio
async def test_todo_entry_tag_addition() -> None:
    mapper = MemoryTodoEntryMapper(storage=_storage)
    repository = TodoEntryRepository(mapper=mapper)

    data = TodoEntry(summary="Lorem ipsum", tags=["doc"], created_at=datetime.now(tz=timezone.utc))
    entity = await repository.create(entity=data)

    tags = ["doc", "secret"]
    entity = await add_tags_to_todo_entry(identifier=entity.id, tags=tags, repository=repository)

    assert len(entity.tags) == 2
