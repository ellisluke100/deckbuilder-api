from deckbuilder.models import CardDB
from pymongo.asynchronous.database import AsyncDatabase
from typing import Optional
from bson import ObjectId


class CardsDatabaseAdapter:
    def __init__(self, db: AsyncDatabase):
        self._db = db

    async def read_one(self, id: str) -> Optional[CardDB]:
        """ Read a single card from the database.

        Args:
            id (str): Card ID.

        Returns:
            Optional[CardDB]: The retrieved card or None if it could not be retrieved.
        """        
        result = await self._db.get_collection("cards").find_one({"_id": ObjectId(id)})

        return CardDB(**result) if result else None

    async def read_multiple(self, limit: int, skip: int) -> list[CardDB]:
        """ Read multiple cards from the database.

        Args:
            limit (int): Maximum number of cards returned.
            skip (int): Number to seek ahead in the returned cards.

        Returns:
            list[CardDB]: List of retrieved cards.
        """        
        results = (
            await self._db.get_collection("cards")
            .find(limit=limit, skip=skip)
            .to_list()
        )

        return [CardDB(**card) for card in results]
