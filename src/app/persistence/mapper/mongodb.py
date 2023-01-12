import os
from random import randint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from entities import TodoEntry
from persistence.mapper.errors import EntityNotFoundMapperError, CreateMapperError, UpdateMapperError
from persistence.mapper.interfaces import TodoEntryMapperInterface


CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING', '')


class MongoDBTodoEntryMapper(TodoEntryMapperInterface):
   _client: MongoClient

   def __init__(self, fixture: dict = None):
      fixture = fixture or {}
      
      self._client = MongoClient(CONNECTION_STRING)
      self._db = self._client.mydb
      self._collection = self._db.todoentries

      for entity in fixture:
         self._insert_entity(entity=entity)

   def close(self):
      self._client.close()
      
   def __enter__(self):
      return self

   def __exit__(self, exc_type, exc_value, exc_traceback):
      self.close()

   async def get(self, identifier: int) -> TodoEntry:
      res = self._collection.find_one(identifier)
      if not res:
         raise EntityNotFoundMapperError(f"Entity `id:{identifier}` was not found.")
      
      return TodoEntry.from_json(**res)

   async def create(self, entity: TodoEntry) -> TodoEntry:
      try:
         identifier = randint(1, 10_000)
         entity.id = identifier
         while not self._insert_entity(entity=entity):
            identifier = randint(1, 10_000)
            entity.id = identifier

         return entity
      except TypeError as error:
         raise CreateMapperError(error)

   async def update(self, entity: TodoEntry) -> TodoEntry:
      try:
         data = dict(entity).copy()
         identifier = data.pop('id')
         self._collection.update_one({"_id": identifier}, {"$set": data})
         return entity
      except TypeError as error:
         raise UpdateMapperError(error)

   def _insert_entity(self, entity: TodoEntry) -> bool:
      try:
         data = entity.to_db()
         self._collection.insert_one(data)
         return True
      except DuplicateKeyError:
         return False

   
  