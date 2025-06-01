from fastapi import APIRouter, Depends, status
from typing import Annotated

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
async def create_user():
    pass