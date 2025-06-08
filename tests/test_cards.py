from fastapi.testclient import TestClient
from deckbuilder.main import app
from deckbuilder.core.database import get_db
import pytest
from mongomock_motor import AsyncMongoMockClient

@pytest.fixture()
def app_client():
    db_client = AsyncMongoMockClient(host="localhost", port=27017)

    def get_db_client():
        yield db_client["test"]

    app.dependency_overrides[get_db] = get_db_client

    return TestClient(app)


@pytest.mark.asyncio
async def test_get_cards_endpoint(app_client):
    response = app_client.get("/cards/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_decks_endpoint(app_client):
    response = app_client.get("/decks/")
    assert response.status_code == 200