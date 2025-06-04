from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
import os
from deckbuilder.core.config import config


client: AsyncMongoClient = None


def get_db() -> AsyncDatabase:
    """Get a database connection.

    Returns:
        AsyncDatabase: Database connection.
    """

    return client.get_database("deckbuilder")


def mongo_startup():
    """
    Open MongoDB connection
    """
    global client
    mongo_addr = config.mongo_addr
    client = AsyncMongoClient(mongo_addr)


def mongo_shutdown():
    """
    Close MongoDB connection
    """
    global client
    if client is None:
        return

    client.close()  # Smelly warning about not awaiting this
    client = None  # Make sure we don't try and use it again
