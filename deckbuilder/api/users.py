from fastapi import APIRouter, Depends, status
from typing import Annotated
from deckbuilder.core.auth import create_user_dep
from deckbuilder.models import User

router = APIRouter(prefix="/users", tags=["users"])

# TODO - this is not that appropriate as a way to get users defined - no real checking goes on


# Quick 'register user' endpoint
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user=Depends(create_user_dep)) -> User:
    return user
