from deckbuilder.models import CardDB
from pymongo.asynchronous.database import AsyncDatabase
from typing import Optional
from bson import ObjectId


# ! - can we split generic stuff out into base?
class CardsDatabaseAdapter:
    def __init__(self, db: AsyncDatabase):
        self._db = db

    # ! Should it be expecting a str here? Or an ObjectId?
    async def read_one(self, id: str) -> Optional[CardDB]:
        """Read a single card from the database.

        Args:
            id (str): _description_

        Returns:
            Optional[CardDB]: _description_
        """
        result = await self._db.get_collection("cards").find_one({"_id": ObjectId(id)})

        return CardDB(**result) if result else None

    async def read_multiple(self, limit: int, skip: int) -> list[CardDB]:
        """Read multiple cards from the database.

        Args:
            limit (int, optional): _description_. Defaults to 10.
            skip (int, optional): _description_. Defaults to 0.
        """
        results = (
            await self._db.get_collection("cards")
            .find(limit=limit, skip=skip)
            .to_list()
        )

        return [CardDB(**card) for card in results]
