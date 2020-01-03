# -*- coding: utf-8 -*-
"""MongoDB database manager."""

import os
import pymongo

from dotenv import load_dotenv
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

# The database manager requires environment variables which have not yet
# been loaded, so load them here.
load_dotenv()


class Database(object):
    """A class for interacting with a MongoDB database.

    Attributes:
        Database.URI: The database location.
        Database.DATABASE: The database cursor.
    """

    URI = os.environ.get('MONGODB_URI')
    print(f'URI = {URI}')
    DB = pymongo.MongoClient(URI).get_database()

    @staticmethod
    def find_many(collection: str, query: dict) -> pymongo.cursor:
        """Fetches multiple documents from the database.

        Args:
            collection: The collection to fetch from.
            query: The search parameters.

        Returns:
            An iterable PyMongo Cursor pointing to the requested documents.
        """
        return Database.DB[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: dict) -> dict:
        """Fetches a single document from the database.

        Args:
            collection: The collection to fetch from.
            query: The search parameters.

        Returns:
            The first document encountered which matches the search parameters.
        """
        return Database.DB[collection].find_one(query)

    @staticmethod
    def insert_one(collection: str, document: dict) -> InsertOneResult:
        """Inserts a document into the database.

        Args:
            collection: The collection to insert into.
            document: The document to be inserted.
        """
        return Database.DB[collection].insert_one(document)

    @staticmethod
    def delete_all(collection: str) -> DeleteResult:
        """Deletes all documents from a collection in the database.

        Args:
            collection: The collection to delete from.
        """
        return Database.DB[collection].delete_many({})

    @staticmethod
    def delete_many(collection: str, query: dict) -> DeleteResult:
        """Deletes a set of documents from the database.

        Args:
            collection: The collection to delete from.
            query: Parameters defining the documents to be deleted.
        """
        return Database.DB[collection].delete_many(query)

    @staticmethod
    def delete_one(collection: str, query: dict) -> DeleteResult:
        """Deletes a single document from the database.

        Args:
            collection: The collection to delete from.
            query: Parameters defining the document to be deleted.
        """
        return Database.DB[collection].delete(query)

    @staticmethod
    def update_one(collection: str, query: dict, document: dict) -> UpdateResult:
        """Upserts a document in the database.

            Updates a document in the database ar creates a new document when no
            existing documents match the search parameters.

        Args:
            collection: The collection containing the document to be updated.
            query: Parameters defining the document to be updated.
            document: The document to be upserted.
        """
        return Database.DB[collection].update_one(query, {'$set': document},
                                                  upsert=True)