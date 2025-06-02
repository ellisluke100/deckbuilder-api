from deckbuilder.models import UserDB
from pymongo.asynchronous.database import AsyncDatabase
from pymongo import ReturnDocument
from typing import Optional
from bson import ObjectId


# TODO - there is an unimaginable amount of reuse here and with these 'Adapter' classes.


class UserDatabaseAdapter:
    def __init__(self, db: AsyncDatabase):
        self._db = db

    async def read_user_by_name(self, username: str) -> Optional[UserDB]:
        """Read a user from the database by name

        Args:
            username (str): User name to search for

        Returns:
            Optional[UserDB]: The retrieved user or None if the user could not be found
        """
        user = await self._db.get_collection("users").find_one({"name": username})

        return UserDB(**user) if user else None

    async def create_one(self, user: dict) -> Optional[UserDB]:
        """Create a user.

        Args:
            user (dict): User info

        Returns:
            Optional[UserDB]: Created user or None if the user could not be created
        """
        db_user = UserDB(**user)

        result = await self._db.get_collection("users").insert_one(
            db_user.model_dump(exclude=["id"])
        )

        if not (user_id := result.inserted_id):
            return None

        object = await self._db.get_collection("users").find_one({"_id": user_id})

        return UserDB(**object)
