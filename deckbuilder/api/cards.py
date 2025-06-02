"""
Endpoints relating to card resources.
"""

from fastapi import APIRouter, Depends, status
from typing import Annotated
from deckbuilder.schemas import CardResponse, CardListResponse
from deckbuilder.core.dependencies import get_cards_dep, get_card_by_id_dep

router = APIRouter(prefix="/cards", tags=["cards"])


@router.get(
    "/",
    description="Get multiple cards.",
    response_description="List of retrieved cards.",
    status_code=status.HTTP_200_OK,
    response_model=CardListResponse,
    response_model_by_alias=False,
)
async def get_cards(
    cards: Annotated[CardListResponse, Depends(get_cards_dep)],
) -> CardListResponse:
    """
    Get cards endpoint.
    """
    # ? Note: Pydantic will do ANOTHER validation / conversion to CardListResponse, because we've defined the response model AND are converting it here
    return cards


@router.get(
    "/{id}",
    description="Get a card by id.",
    response_description="The retrieved card.",
    status_code=status.HTTP_200_OK,
    response_model=CardResponse,
    response_model_by_alias=False,
)
async def get_card_by_id(
    card: Annotated[CardResponse, Depends(get_card_by_id_dep)],
) -> CardResponse:
    """
    Get a card by id endpoint.
    """
    return card
