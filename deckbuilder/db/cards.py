from deckbuilder.models import CardDB
from pymongo.asynchronous.database import AsyncDatabase
from typing import Optional
from deckbuilder.db.base import BaseDatabase


class CardsDatabase(BaseDatabase):
    def __init__(self, db: AsyncDatabase):
        super().__init__(db)

    async def read_one(self, id: str) -> Optional[CardDB]:
        """Read a single card from the database.

        Args:
            id (str): Card ID.

        Returns:
            Optional[CardDB]: The retrieved card or None if it could not be retrieved.
        """
        result = await self._read_document_by_id(id, "cards")

        return CardDB(**result) if result else None

    async def read_multiple(
        self, limit: int, skip: int, keywords: list[str]
    ) -> list[CardDB]:
        """Read multiple cards from the database.

        Args:
            limit (int): Maximum number of cards returned.
            skip (int): Number to seek ahead in the returned cards.

        Returns:
            list[CardDB]: List of retrieved cards.
        """
        results = await self._read_documents(limit, skip, "cards")

        return [CardDB(**card) for card in results]
