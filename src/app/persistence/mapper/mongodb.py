from pymongo import MongoClient

from entities import TodoEntry
from persistence.mapper.errors import EntityNotFoundMapperError, CreateMapperError, UpdateMapperError
from persistence.mapper.interfaces import TodoEntryMapperInterface


class MongoDBTodoEntryMapper(TodoEntryMapperInterface):
   _client: MongoClient

   def __init__(self, connection_string: str):
      CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
      self._client = MongoClient(CONNECTION_STRING)
  