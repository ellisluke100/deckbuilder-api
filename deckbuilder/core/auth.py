from fastapi import Security, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from deckbuilder.models import Token, UserDB
from deckbuilder.db.users import UserDatabaseAdapter
from deckbuilder.core.dependencies import get_db
from typing import Optional
from passlib.context import CryptContext
from fastapi import HTTPException
import jwt

# Token url -> user + password -> get a bearer token -> use token in requests -> good to go
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# From https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(username: str, password: str, db = Depends(get_db)) -> Optional[UserDB]:
    """_summary_

    Args:
        username (str): _description_
        password (str): _description_
        db (_type_, optional): _description_. Defaults to Depends(get_db).

    Returns:
        Optional[UserDB]: _description_
    """    
    adapter = UserDatabaseAdapter(db=db)

    user = adapter.read_user_by_name(username)

    # Check if user exists
    if not user:
        return None  
    
    # Check if passwords match
    if not pwd_context.verify(password, user.secret_password):
        return None
    
    return user


async def create_token(data: dict) -> Token:
    """_summary_

    Args:
        data (dict): _description_

    Returns:
        Token: _description_
    """    
    encoded_jwt = jwt.encode(
        payload={"exp":-1} | data.copy(),
        secret="my_secret", # Oh no
        algorithm="RS256"
    )
    return Token(
        token=encoded_jwt,
        type="bearer"
    )


async def get_token_dep(form = Depends(OAuth2PasswordRequestForm)) -> Token:
    """_summary_

    Args:
        form (_type_, optional): _description_. Defaults to Depends(OAuth2PasswordRequestForm).

    Raises:
        HTTPException: _description_

    Returns:
        Token: _description_
    """    
    user = authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed."
        )
    
    token = create_token(
        {"sub": user.username}
    )
    return token
    


async def get_current_user(token = Depends(oauth2_scheme)):
    pass


