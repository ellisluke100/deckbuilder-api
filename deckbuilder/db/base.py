from deckbuilder.models import DeckDB
from pymongo.asynchronous.database import AsyncDatabase
from pymongo import ReturnDocument
from typing import Optional
from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult


class BaseDatabase:
    """
    Base class for providing common database operations.
    """
    def __init__(self, db: AsyncDatabase):
        self._db = db

    # ! Should this actually be generic in the sense of it can be any field not just id
    async def _read_document_by_id(self, id: str, collection: str) -> Optional[dict]:
        """ Retrieve a document from the collection by its ID

        Args:
            id (str): ID of the document to retrieve
            collection (str): The MongoDB collection to look in

        Returns:
            Optional[dict]: The retrieved document or None if it could not be retrieved
        """        
        return await self._db.get_collection(collection).find_one({"_id": ObjectId(id)})

    # TODO - query params should probably be an object or similar (not defined willy nilly in every function)
    async def _read_documents(self, limit: int, skip: int, collection: str) -> list[dict]:
        """ Retrieve multiple documents according to query parameters and pagination

        Args:
            limit (int): Maximum number of documents to retrieve
            skip (int): Document number to seek ahead to in retrieved documents
            collection (str): The MongoDB collection to look in

        Returns:
            list[dict]: List of retrieved documents
        """        
        return await self._db.get_collection(collection).find().limit(limit).skip(skip).to_list()

    async def _create_document(self, fields: dict, collection: str) -> InsertOneResult:
        """ Create a new document in the collection..

        Args:
            fields (dict): Document to create
            collection (str): The MongoDB collection to create a document in.

        Returns:
            dict: The created document
        """        
        return await self._db.get_collection(collection).insert_one(fields)

    async def _delete_document_by_id(self, id: str, collection: str) -> DeleteResult:
        """ Delete a document from a colleciton by it's ID.

        Args:
            id (str): ID of the document to delete
            collection (str): The MongoDB collection delete a document from.

        Returns:
            _type_: _description_
        """        
        return await self._db.get_collection(collection).delete_one({"_id": ObjectId(id)})
    
    async def _update_document(self, id: str, fields: dict, collection: str) -> Optional[dict]:
        """ Update a document in the collection by its ID.

        Args:
            id (str): ID of the document to update.
            fields (dict): Fields to update the document with
            collection (str): The MongoDB collection to update the document in

        Returns:
            Optional[dict]: The updated document or None if it couldn't update
        """        
        return self._db.get_collection(collection).find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": fields},
            return_document=ReturnDocument.AFTER,  # Returns the bson document after its been updated - maybe this should be configurable?
        )
