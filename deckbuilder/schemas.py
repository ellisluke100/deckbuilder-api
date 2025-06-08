from pydantic import BaseModel, Field, ConfigDict, AfterValidator
from deckbuilder.models import CardKeyword
from bson import ObjectId
from typing import Annotated
from deckbuilder.core.utils import is_valid_object_id

# We need some base classes here pleeassee

ValidId = Annotated[str, AfterValidator(is_valid_object_id)]

#########
# Cards #
#########


class CardResponse(BaseModel):
    """
    Schema for returning a Card.
    """

    id: str = Field(alias="_id")
    name: str = Field()
    cost: int = Field(gt=0)
    power: int = Field()
    text: str = Field()
    keywords: list[CardKeyword] = Field()

    model_config = ConfigDict(validate_by_name=True)


class CardListResponse(BaseModel):
    """
    Schema for returning a lsit of Cards.
    """

    cards: list[CardResponse]


class CommonQueryParameters(BaseModel):
    limit: int = Field(default=10)
    skip: int = Field(default=0)


class CardQueryParameters(CommonQueryParameters):
    keywords: list[CardKeyword] = Field(default=[])


#########
# Decks #
#########


class DeckBase(BaseModel):
    name: str = Field()
    cards: list[ValidId] = Field(max_length=6, default=[])  # List of IDs


class DeckCreateRequest(DeckBase):
    """
    Schema for creating a Deck.
    """


class DeckUpdateRequest(BaseModel):
    """
    Schema for updating a Deck
    """

    name: str = Field(default=None)  # Rename
    cards: list[ValidId] = Field(
        max_length=6, default=[]
    )  # Change cards that are in the deck


class DeckResponse(BaseModel):
    """
    Schema for returning a Deck.
    """

    id: str = Field(alias="_id")
    name: str = Field()
    cards: list[str] = Field(max_length=6)

    model_config = ConfigDict(validate_by_name=True, json_encoders={ObjectId: str})


class DeckDetailResponse(BaseModel):
    """
    Schema for returning a Deck.
    """

    id: str = Field(alias="_id")
    name: str = Field()
    cards: list[CardResponse] = Field(max_length=6)

    model_config = ConfigDict(validate_by_name=True, json_encoders={ObjectId: str})


class DeckListResponse(BaseModel):
    """
    Schema for returning a list of Decks.
    """

    decks: list[DeckResponse] = Field()


#########
# Users #
#########

# TODO Use Pydantic secret field perhaps


class UserCreateRequest(BaseModel):
    """
    Schema for creating a User.
    """

    username: str = Field()
    password: str = Field()
