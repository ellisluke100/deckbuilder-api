from deckbuilder.db.cards import CardsDatabase
from deckbuilder.db.decks import DeckDatabase
from deckbuilder.models import DeckDB
from fastapi import Depends, HTTPException, status
from deckbuilder.core.database import get_db
from deckbuilder.schemas import (
    CardResponse,
    CardListResponse,
    DeckResponse,
    DeckListResponse,
    DeckCreateRequest,
    DeckUpdateRequest,
    DeckDetailResponse,
)

# TODO - split this file out or something
# TODO - make reusable deps - theres a lot of code reuse in here

#########
# CARDS #
#########


async def get_cards_dep(
    limit: int = 10, skip: int = 0, db=Depends(get_db)
) -> CardListResponse:
    """Get cards.

    Args:
        limit (int, optional): Query parameter for restricting number of card results returned. Defaults to 10.
        skip (int, optional): Query parameter for seeking ahead in the card results returned. Defaults to 0.
        db (_type_, optional): Database connection. Defaults to Depends(get_db).

    Returns:
        CardListResponse: Model for list of cards.
    """
    adapter = CardsDatabase(db=db)

    results = await adapter.read_multiple(limit, skip)

    return CardListResponse(
        cards=[CardResponse(**card.model_dump()) for card in results]
    )


async def get_card_by_id_dep(id: str, db=Depends(get_db)) -> CardResponse:
    """Get card by it's ID.

    Args:
        id (str): ID of the card to get.
        db (_type_, optional): Database connection. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 response if the card can't be found.

    Returns:
        CardResponse: Model for returning a card.
    """
    adapter = CardsDatabase(db=db)

    result = await adapter.read_one(id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Card {id} not found."
        )

    return CardResponse(**result.model_dump())


async def get_cards_by_id(
    card_ids: list[str], db=Depends(get_db)
) -> list[CardResponse]:
    """Get multiple cards by their IDs.

    Args:
        card_ids (list[str]): List of card IDs.
        db (_type_, optional): Database connection. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if any cards can't be found.

    Returns:
        list[CardResponse]: List of card models to return.
    """
    card_adapter = CardsDatabase(db=db)

    cards = []
    for id in card_ids:
        card = await card_adapter.read_one(id)

        if not card:
            # ! User is trying to get a deck here; if a card can't be found, do we actually just raise a 404 or just not have a card view there
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Card {id} not found."
            )

        cards.append(CardResponse(**card.model_dump()))

    return cards


#########
# DECKS #
#########


async def get_decks_dep(
    limit: int = 10, skip: int = 0, db=Depends(get_db)
) -> DeckListResponse:
    """Get decks.

    Args:
        limit (int, optional): Query parameter for restricting number of deck results returned. Defaults to 10.
        skip (int, optional): Query parameter for seeking ahead in the deck results returned. Defaults to 0.
        db (_type_, optional): Database connection. Defaults to Depends(get_db).

    Returns:
        DeckListResponse: List of decks.
    """
    adapter = DeckDatabase(db=db)

    results = await adapter.read_multiple(limit, skip)

    return DeckListResponse(
        decks=[DeckResponse(**deck.model_dump()) for deck in results]
    )


async def get_deck_by_id_dep(id: str, db=Depends(get_db)) -> DeckDetailResponse:
    """Get a deck by it's ID.

    Args:
        id (str): ID of the deck to get.
        db (_type_, optional): Database connection. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if the deck couldn't be found.

    Returns:
        DeckDetailResponse: Detail view of the deck retrieved.
    """
    adapter = DeckDatabase(db=db)

    result = await adapter.read_one(id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Deck {id} not found."
        )

    cards = await get_cards_by_id(result.cards, db)

    return DeckDetailResponse(**result.model_dump(exclude=["cards"]), cards=cards)


async def create_deck_dep(deck: DeckCreateRequest, db=Depends(get_db)) -> DeckResponse:
    """Create a new deck.

    Args:
        deck (DeckCreateRequest): Request containing info about deck to create.
        db (_type_, optional): Database connetion. Defaults to Depends(get_db).

    Returns:
        DeckResponse: Deck retrieved.
    """
    adapter = DeckDatabase(db=db)

    result = await adapter.create_one(DeckDB(**deck.model_dump()))

    return DeckResponse(**result.model_dump())


async def delete_deck_dep(id: str, db=Depends(get_db)) -> None:
    """Delete a deck.

    Args:
        id (str): Deck ID
        db (_type_, optional): Database connection. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if the deck could not be found.
    """
    adapter = DeckDatabase(db=db)

    if not (await adapter.read_one(id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Deck {id} not found."
        )

    # ! Is this right
    await adapter.delete_one(id)

    return


async def update_deck_dep(
    id: str, update_fields: DeckUpdateRequest, db=Depends(get_db)
) -> DeckResponse:
    """_summary_

    Args:
        id (str): Deck ID
        update_fields (DeckUpdateRequest): Fields to update in the corresponding Deck
        db (_type_, optional): Database connection. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if the deck could not be found.

    Returns:
        DeckResponse: The updated Deck
    """
    adapter = DeckDatabase(db=db)
    fields = update_fields.model_dump(exclude_unset=True)

    # Nothing to update; just return the found object
    if not fields:
        deck = await adapter.read_one(id)

        if not deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Deck {id} not found."
            )

        deck = DeckDB(**deck)
        return DeckResponse(**deck.model_dump())

    # Update the object
    updated_deck = await adapter.update_one(id, fields)

    if not updated_deck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Deck {id} not found."
        )

    return DeckResponse(**updated_deck.model_dump())


#########
# MISC  #
#########


async def validate_id():
    pass


async def validate_card_id():
    pass


async def validate_deck_id():
    pass
