from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from typing import Annotated, Optional
from enum import Enum

# https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/
PyObjectId = Annotated[str, BeforeValidator(str)]

#########
# Cards #
#########


class CardKeyword(str, Enum):
    """
    Card keyword.
    """

    ON_REVEAL = "on_reveal"
    ONGOING = "ongoing"
    DISCARD = "discard"
    MOVE = "move"
    DESTROY = "destroy"


class CardDB(BaseModel):
    """
    Model representing a Card.
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    name: str = Field()
    cost: int = Field(gt=0)
    power: int = Field()
    text: str = Field()
    keywords: list[CardKeyword] = Field()
    # TODO image: image type

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Blade",
                "cost": 1,
                "power": 3,
                "text": "On reveal: Discard the rightmost card in your hand.",
                "keywords": ["on_reveal", "discard"],
            }
        },
    )


#########
# Decks #
#########


class DeckDB(BaseModel):
    """
    Model representing a Deck of Cards
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    name: str = Field()
    cards: list[PyObjectId] = (
        Field()
    )  # List of PyObjectId's so we can perform lookup during GET request
    # user: user id

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "My first deck",
                "cards": ["id_1", "id_2", "id_3"],  # These are actually ObjectId's
            }
        },
    )


#########
# Users #
#########


class AccessToken(BaseModel):
    username: str = Field(default=None)


class Token(BaseModel):
    """
    Model for an access token.
    """

    token: str = Field()
    type: str = Field()


class User(BaseModel):
    """
    Model for user.
    """

    # TODO - id
    username: str = Field()


class UserDB(User):
    """
    Model for user in database.
    """

    secret_password: str = Field()
