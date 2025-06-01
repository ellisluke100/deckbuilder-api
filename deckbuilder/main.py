from fastapi import FastAPI
from contextlib import asynccontextmanager
from deckbuilder.api import cards, decks, token, users
from deckbuilder.core.database import mongo_startup, mongo_shutdown


def startup(app: FastAPI):
    """Things to do on app startup

    Args:
        app (FastAPI): app instance
    """
    mongo_startup()


def shutdown(app: FastAPI):
    """Things to do before app shutdown

    Args:
        app (FastAPI): app instance
    """
    mongo_shutdown()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Define things to do before and after FastAPI app runs.

    Args:
        app (FastAPI): app instance
    """
    startup(app)

    yield

    shutdown(app)


def get_app() -> FastAPI:
    """Create a new FastAPI app instance.

    Returns:
        FastAPI: app instance
    """
    new_app = FastAPI(
        title="Deckbuilder",
        description="Build a deck from definitely-not Marvel Snap cards",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Routers
    new_app.include_router(cards.router)
    new_app.include_router(decks.router)
    new_app.include_router(token.router)
    new_app.include_router(users.router)

    return new_app


# FastAPI instance
app = get_app()
