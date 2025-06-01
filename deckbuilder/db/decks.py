from deckbuilder.models import DeckDB
from pymongo.asynchronous.database import AsyncDatabase
from pymongo import ReturnDocument
from typing import Optional
from bson import ObjectId

# ! I dont like handling model conversion here


class DeckDatabaseAdapter:
    def __init__(self, db: AsyncDatabase):
        self._db = db

    async def read_one(self, id: str) -> Optional[DeckDB]:
        """_summary_

        Args:
            id (str): _description_

        Returns:
            Optional[DeckDB]: _description_
        """
        result = await self._db.get_collection("decks").find_one({"_id": ObjectId(id)})

        return DeckDB(**result) if result else None

    async def read_multiple(self, limit: int, skip: int) -> list[DeckDB]:
        """_summary_

        Args:
            limit (int): _description_
            skip (int): _description_

        Returns:
            list[DeckDB]: _description_
        """
        results = (
            await self._db.get_collection("decks")
            .find(limit=limit, skip=skip)
            .to_list()
        )

        return [DeckDB(**deck) for deck in results]

    async def create_one(self, deck: DeckDB) -> Optional[DeckDB]:
        """_summary_

        Args:
            deck (DeckDB): _description_

        Returns:
            DeckDB: _description_
        """
        result = await self._db.get_collection("decks").insert_one(
            deck.model_dump(exclude=["id"])
        )

        if not (deck_id := result.inserted_id):
            return None

        object = await self._db.get_collection("decks").find_one({"_id": deck_id})

        return DeckDB(**object)

    async def delete_one(self, id: str) -> bool:
        """_summary_

        Args:
            id (str): _description_

        Returns:
            bool: _description_
        """
        result = await self._db.get_collection("decks").delete_one(
            {"_id": ObjectId(id)}
        )

        if not result.deleted_count == 1:
            return False

        return True

    async def update_one(self, id: str, fields: dict) -> DeckDB:
        """_summary_

        Args:
            id (str): _description_
            fields (dict): _description_

        Returns:
            DeckDB: _description_
        """
        result = await self._db.get_collection("decks").find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": fields},
            return_document=ReturnDocument.AFTER,
        )

        return DeckDB(**result)
