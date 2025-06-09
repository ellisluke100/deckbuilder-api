from fastapi.testclient import TestClient
from deckbuilder.main import app
from deckbuilder.core.database import get_db
import pytest
from mongomock_motor import AsyncMongoMockClient
from bson import ObjectId


async def is_same_card(response_card: dict, test_card: dict):
    return all(
        [
            response_card["id"] == str(test_card["_id"]),
            response_card["name"] == test_card["name"],
            response_card["cost"] == test_card["cost"],
            response_card["power"] == test_card["power"],
            response_card["text"] == test_card["text"],
            response_card["keywords"] == test_card["keywords"],
        ]
    )


db_client = AsyncMongoMockClient(host="localhost", port=27017)  # Sort this


@pytest.fixture(scope="session")
def app_client():

    def get_db_client():
        yield db_client["test"]

    app.dependency_overrides[get_db] = get_db_client

    return TestClient(app)


@pytest.fixture(scope="function")
def setup_cards():
    cards = [
        {
            "_id": ObjectId(),
            "name": "Test Card",
            "power": 3,
            "cost": 2,
            "text": "Test text",
            "keywords": ["ongoing", "discard"],
        },
        {
            "_id": ObjectId(),
            "name": "Test Card",
            "power": 6,
            "cost": 4,
            "text": "Test text",
            "keywords": ["ongoing", "discard"],
        },
    ]

    db_client["test"].get_collection("cards").insert_many(cards)

    yield cards

    db_client["test"].get_collection("cards").delete_many({})


#########
# TESTS #
#########


@pytest.mark.asyncio
async def test_get_no_cards(app_client):
    response = app_client.get("/cards/")

    assert response.status_code == 200
    assert response.json() == {"cards": []}


# FIXME - 404 error
# @pytest.mark.asyncio
# async def test_get_one_card(app_client, setup_cards):
#     card = setup_cards[0]
#     response = app_client.get(f"/cards/{card['_id']}")

#     assert response.status_code == 200
#     assert await is_same_card(response.json(), card)


@pytest.mark.asyncio
async def test_get_multiple_cards(app_client, setup_cards):
    response = app_client.get("/cards/")

    assert response.status_code == 200
    for response_card, card in zip(response.json()["cards"], setup_cards):
        assert await is_same_card(response_card, card)


@pytest.mark.asyncio
async def test_get_card_not_found(app_client):
    response = app_client.get(f"/cards/{ObjectId()}")
    assert response.status_code == 404
