from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

# client = AsyncMongoClient("mongo://localhost:8000/") # TODO - configurable
client: AsyncMongoClient = None


def get_db() -> AsyncDatabase:
    """_summary_

    Returns:
        AsyncDatabase: _description_
    """
    return client.get_database("deckbuilder")


def mongo_startup():
    """Open MongoDB connection"""
    global client
    client = AsyncMongoClient("mongodb://localhost:27017")


def mongo_shutdown():
    """Close MongoDB connection"""
    global client
    if client is None:
        return

    client.close()  # Smelly warning about not awaiting this
    client = None
