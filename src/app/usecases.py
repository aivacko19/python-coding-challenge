from typing import List
from entities import TodoEntry
from persistence.errors import CreateError, EntityNotFoundError
from persistence.repository import TodoEntryRepository


class UseCaseError(Exception):
    pass


class NotFoundError(UseCaseError):
    pass


async def get_todo_entry(identifier: int, repository: TodoEntryRepository) -> TodoEntry:
    try:
        return await repository.get(identifier=identifier)
    except EntityNotFoundError as err:
        raise NotFoundError(err)


async def create_todo_entry(
    entity: TodoEntry, repository: TodoEntryRepository
) -> TodoEntry:
    try:
        return await repository.create(entity=entity)
    except CreateError as error:
        raise UseCaseError(error)


async def add_tags_to_todo_entry(identifier: int, tags: List[str], repository: TodoEntryRepository) -> TodoEntry:
    try:
        entity = await repository.get(identifier=identifier)
        for tag in tags:
            if tag not in entity.tags:
                entity.tags.append(tag)
        return await repository.update(entity=entity)
    except EntityNotFoundError as err:
        raise NotFoundError(err)
