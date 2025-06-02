from fastapi import APIRouter, Depends, status
from typing import Annotated
from deckbuilder.schemas import DeckResponse, DeckListResponse, DeckDetailResponse
from deckbuilder.core.dependencies import (
    create_deck_dep,
    delete_deck_dep,
    get_decks_dep,
    get_deck_by_id_dep,
    update_deck_dep,
)

router = APIRouter(prefix="/decks", tags=["decks"])


@router.get(
    "/{id}",
    description="Get a deck by it's ID",
    response_description="The retrieved deck",
    response_model=DeckDetailResponse,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
)
async def get_deck_by_id(
    deck: Annotated[DeckDetailResponse, Depends(get_deck_by_id_dep)],
):
    """ 
    Get a deck by its ID.
    """
    return deck


@router.get(
    "/",
    description="Get multiple decks.",
    response_description="List of retrieved decks.",
    response_model=DeckListResponse,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK
)
async def get_decks(decks: Annotated[DeckListResponse, Depends(get_decks_dep)]):
    """ 
    List decks.
    """
    return decks


@router.post(
    "/",
    description="Create a deck.",
    response_description="The created deck.",
    response_model=DeckResponse,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_deck(new_deck: Annotated[DeckResponse, Depends(create_deck_dep)]):
    """ 
    Create a new deck.
    """
    return new_deck


@router.delete(
    "/{id}", 
    description="Delete a deck.",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_deck(response=Depends(delete_deck_dep)):
    """ 
    Delete a deck.
    """
    return response


@router.put("/{id}",
             description="Update a deck.",
             response_description="The updated deck.",
             status_code=status.HTTP_200_OK)
async def update_deck(deck=Depends(update_deck_dep)):
    """ 
    Update a deck.
    """
    return deck
