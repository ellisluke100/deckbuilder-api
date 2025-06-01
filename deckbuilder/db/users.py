from deckbuilder.models import UserDB
from pymongo.asynchronous.database import AsyncDatabase
from pymongo import ReturnDocument
from typing import Optional
from bson import ObjectId


class UserDatabaseAdapter:
    def __init__(self, db: AsyncDatabase):
        self._db = db

    async def read_user_by_name(self, username: str) -> Optional[UserDB]:
        """_summary_

        Args:
            username (str): _description_

        Returns:
            Optional[UserDB]: _description_
        """        
        user = await self._db.get_collection("users").find_one({"name":username})

        return UserDB(**user) if user else None

