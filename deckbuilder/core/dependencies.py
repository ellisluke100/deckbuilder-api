from deckbuilder.db.cards import CardsDatabaseAdapter
from deckbuilder.db.decks import DeckDatabaseAdapter
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


#########
# CARDS #
#########


async def get_cards_dep(
    limit: int = 10, skip: int = 0, db=Depends(get_db)
) -> CardListResponse:
    """_summary_

    Args:
        limit (int, optional): _description_. Defaults to 10.
        skip (int, optional): _description_. Defaults to 0.
        db (_type_, optional): _description_. Defaults to Depends(get_db).

    Returns:
        list[CardDB]: _description_
    """
    adapter = CardsDatabaseAdapter(db=db)

    # results = await adapter.read_multiple(limit, skip)
    results = await adapter.read_multiple(limit, skip)

    return CardListResponse(
        cards=[CardResponse(**card.model_dump()) for card in results]
    )


async def get_card_by_id_dep(id: str, db=Depends(get_db)) -> CardResponse:
    """_summary_

    Args:
        id (str): _description_
        db (_type_, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        CardDB: _description_
    """
    adapter = CardsDatabaseAdapter(db=db)

    result = await adapter.read_one(id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Card {id} not found."
        )

    return CardResponse(**result.model_dump())


async def get_cards_by_id(card_ids: list[str], db) -> list[CardResponse]:
    """_summary_

    Args:
        ids (list[str]): _description_
        db (_type_, optional): _description_. Defaults to Depends(get_db).

    Returns:
        list[CardResponse]: _description_
    """
    card_adapter = CardsDatabaseAdapter(db=db)

    cards = []
    for id in card_ids:
        card = await card_adapter.read_one(id)

        if not card:
            # ! User is trying to get a deck here; if a card can't be found, do we actually just raise a 404 or just not have a card view there
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Card {id} not found."
            )
        
        cards.append(CardResponse(**card.model_dump()))

    return cards


#########
# DECKS #
#########


async def get_decks_dep(
    limit: int = 10, skip: int = 0, db=Depends(get_db)
) -> DeckListResponse:
    """_summary_

    Args:
        limit (int): _description_
        skip (int): _description_
        db (_type_, optional): _description_. Defaults to Depends(get_db).

    Returns:
        DeckListResponse: _description_
    """
    adapter = DeckDatabaseAdapter(db=db)

    results = await adapter.read_multiple(limit, skip)

    return DeckListResponse(
        decks=[DeckResponse(**deck.model_dump()) for deck in results]
    )


async def get_deck_by_id_dep(id: str, db=Depends(get_db)) -> DeckDetailResponse:
    """_summary_

    Args:
        id (str): _description_
        db (_type_, optional): _description_. Defaults to Depends(get_db).

    Returns:
        DeckResponse: _description_
    """
    adapter = DeckDatabaseAdapter(db=db)

    result = await adapter.read_one(id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deck {id} not found."
        )

    result = DeckDB(**result)
    cards = await get_cards_by_id(result.cards, db)

    return DeckDetailResponse(**result.model_dump(exclude=["cards"]), cards=cards)


async def create_deck_dep(deck: DeckCreateRequest, db=Depends(get_db)) -> DeckResponse:
    """_summary_

    Args:
        deck (DeckCreateRequest): _description_
        db (_type_, optional): _description_. Defaults to Depends(get_db).

    Returns:
        DeckResponse: _description_
    """
    adapter = DeckDatabaseAdapter(db=db)

    result = await adapter.create_one(DeckDB(**deck.model_dump()))

    # ! Should this really contain the cards? I've put IDs in my created object, so the IDs should get returned?
    cards = await get_cards_by_id(result.cards, db)

    return DeckResponse(**result.model_dump(exclude=["cards"]), cards=cards)


async def delete_deck_dep(id: str, db=Depends(get_db)):
    """_summary_

    Args:
        id (str): _description_
        db (_type_, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_
    """
    adapter = DeckDatabaseAdapter(db=db)

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
        id (str): _description_
        update_fields (DeckUpdateRequest): _description_
        db (_type_, optional): _description_. Defaults to Depends(get_db).
    """
    adapter = DeckDatabaseAdapter(db=db)
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
