# -*- coding: utf-8 -*-

"""A base model which all other models inherit from."""

from abc import ABCMeta, abstractmethod
from typing import Dict, List , Type, TypeVar, Union

from common.database import Database

T = TypeVar('T', bound='Model')


class Model(metaclass=ABCMeta):
    """A base class from which all other models inherit.

    Attributes:
            _db_collection: The database collection where this object is stored.
            _id: The unique identifier of this object.
    """

    _db_collection: str
    _id: str

    def __init__(self, *args, **kwargs) -> None:
        pass

    def delete(self):
        """Deletes an object from the database."""
        return Database.delete_one(self._db_collection, {'_id': self._id})

    def save_to_db(self):
        """Saves the object to the database."""
        return Database.update_one(self._db_collection, {'_id': self._id},
                                   self.json())

    @classmethod
    def fetch_all(cls: Type[T]) -> List[T]:
        """Fetches all objects from the database."""
        documents = Database.find_many(cls._db_collection, {})
        return [cls(**document) for document in documents]

    @classmethod
    def fetch_by_id(cls: Type[T], _id: str) -> T:
        """Fetches one object from the database."""
        return cls.find_one('_id', _id)

    @classmethod
    def find_many(cls: Type[T], attribute: str,
                  value: Union[str, Dict]) -> List[T]:
        """Searches the database for a set of documents."""
        documents = Database.find_many(cls._db_collection, {attribute: value})
        return [cls(**document) for document in documents]

    @classmethod
    def find_one(cls: Type[T], attribute: str, value: Union[str, Dict]) -> T:
        """Searches the database for a single object."""
        return cls(**Database.find_one(cls._db_collection, {attribute: value}))

    @abstractmethod
    def json(self) -> Dict:
        """Creates a dict from model attributes which are stored in the db."""
        raise NotImplementedError
