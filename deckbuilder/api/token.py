from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from deckbuilder.models import Token
from deckbuilder.core.auth import get_token_dep

router = APIRouter(tags=["cards"])

@router.post("/token")
async def get_token(token = Depends(get_token_dep)) -> Token:
    """ """
    return token