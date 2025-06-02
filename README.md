## Deckbuilder RESTful API

View Marvel Snap cards and build a deck. For-fun project :)

Features:
- View cards
- Manage decks (CRUD operations)

To-Do:
- Unit Tests (probably should have done TDD)
- Authentication (OAuth2 tokens password bearer)
- Full containerized environment
- Deck strength analytics

## Prerequisites

- Python >=3.13
- Poetry
- Docker

## Test environment

Setup environment:

```bash 
docker compose up -d --build 
```

Make a request, e.g.:

```bash
curl -X GET localhost:8000/cards/ | jq
```

Tear down environment:

```bash
docker compose down -v 
```

## Technologies used

- Python
- FastAPI (uvicorn)
- MongoDB (PyMongo)
- Docker compose
- Poetry
- Black
