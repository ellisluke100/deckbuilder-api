from fastapi import APIRouter, Depends, status
from typing import Annotated
from deckbuilder.models import Token
from deckbuilder.core.auth import get_token_dep

router = APIRouter(tags=["cards"])

@router.post("/token",
             description="Get an access token.",
             response_description="An access token for the given user credentials.",
             status_code=status.HTTP_200_OK) # Does the standard say anything different for the status code
async def get_token(token = Depends(get_token_dep)) -> Token:
    """ 
    Get an access token for the given user credentials.
    """
    return token