from deckbuilder.models import DeckDB
from pymongo.asynchronous.database import AsyncDatabase
from pymongo import ReturnDocument
from typing import Optional
from bson import ObjectId

# ! What does get_collection() actually do? Am I thrashing the DB by calling that every time?


class DeckDatabaseAdapter:
    def __init__(self, db: AsyncDatabase):
        self._db = db

    async def read_one(self, id: str) -> Optional[DeckDB]:
        """ Read a deck from the database.

        Args:
            id (str): Deck ID

        Returns:
            Optional[DeckDB]: Retrieved deck or None if the deck could not be found
        """        
        result = await self._db.get_collection("decks").find_one({"_id": ObjectId(id)})

        return DeckDB(**result) if result else None

    async def read_multiple(self, limit: int, skip: int) -> list[DeckDB]:
        """ Read multiple decks from the database.

        Args:
            limit (int): Maxmimum number of decks retreived
            skip (int): Skip ahead in the decks retrieved

        Returns:
            list[DeckDB]: List of decks retrieved
        """  
        results = (
            await self._db.get_collection("decks")
            .find(limit=limit, skip=skip)
            .to_list()
        )

        return [DeckDB(**deck) for deck in results]

    # ! I thought this should handle the db model conversion? For the deck arg
    async def create_one(self, deck: DeckDB) -> Optional[DeckDB]:
        """ Create a deck in the database

        Args:
            deck (DeckDB): Deck to create.

        Returns:
            Optional[DeckDB]: The created deck or None if it couldn't be created.
        """        
        result = await self._db.get_collection("decks").insert_one(
            deck.model_dump(exclude=["id"])
        )

        if not (deck_id := result.inserted_id):
            return None

        object = await self._db.get_collection("decks").find_one({"_id": deck_id})

        return DeckDB(**object)

    async def delete_one(self, id: str) -> bool:
        """ Delete a deck from the database.

        Args:
            id (str): Deck ID

        Returns:
            bool: Whether the delete was successful or not
        """        
        result = await self._db.get_collection("decks").delete_one(
            {"_id": ObjectId(id)}
        )

        if not result.deleted_count == 1:
            return False

        return True

    async def update_one(self, id: str, fields: dict) -> DeckDB:
        """ Update a deck in the database

        Args:
            id (str): Deck ID
            fields (dict): Fields to update with

        Returns:
            DeckDB: The updated deck
        """        
        result = await self._db.get_collection("decks").find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": fields},
            return_document=ReturnDocument.AFTER, # Returns the bson document after its been updated
        )

        return DeckDB(**result)
