from fastapi import Security, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from deckbuilder.models import Token, UserDB
from deckbuilder.db.users import UserDatabaseAdapter
from deckbuilder.core.dependencies import get_db
from typing import Optional
from passlib.context import CryptContext
from fastapi import HTTPException
import jwt
from deckbuilder.models import User
from deckbuilder.schemas import UserCreateRequest

# Token url -> user + password -> get a bearer token -> use token in requests -> good to go
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# From https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(
    username: str, password: str, db=Depends(get_db)
) -> Optional[UserDB]:
    """Authenticate a user.

    Args:
        username (str): Username
        password (str): User's password
        db (_type_, optional): Database connection. Defaults to Depends(get_db).

    Returns:
        Optional[UserDB]: The authenticated user or None if authentication failed.
    """
    adapter = UserDatabaseAdapter(db=db)

    user = await adapter.read_user_by_name(username)

    # Check if user exists
    if not user:
        return None

    # Check if passwords match
    if not pwd_context.verify(password, user.secret_password):
        return None

    return user


async def create_token(data: dict) -> Token:
    """Create a JWT-encoded access token.

    Args:
        data (dict): Data to encode as a JWT.

    Returns:
        Token: The token with encoded JWT.
    """
    encoded_jwt = jwt.encode(
        payload={"exp": -1} | data.copy(),
        secret="my_secret",  # Oh no
        algorithm="RS256",
    )
    return Token(token=encoded_jwt, type="bearer")


async def get_token_dep(form=Depends(OAuth2PasswordRequestForm)) -> Token:
    """Get an access token for given user information.

    Args:
        form (_type_, optional): User credentials form. Defaults to Depends(OAuth2PasswordRequestForm).

    Raises:
        HTTPException: 401 if user failed to authenticate.

    Returns:
        Token: The created access token.
    """
    user = authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed.")

    # Is 'sub' definitely in the JWT standard?
    token = create_token({"sub": user.username})
    return token


async def secretify(plaintext: str) -> str:
    """Convert plaintext to secret

    Args:
        password (str): Plaintext to make secret

    Returns:
        str: The secret converted from plaintext
    """
    return pwd_context.hash(plaintext)


async def get_current_user(token=Depends(oauth2_scheme)):
    pass


# TODO - I dont think this is the appropriate place to put this

#########
# USERS #
#########


async def create_user_dep(user: UserCreateRequest, db=Depends(get_db)) -> User:
    """Create a user.

    Args:
        user (UserCreateRequest): User to create
        db (_type_, optional): Database connection. Defaults to Depends(get_db).

    Returns:
        User: Created user
    """
    adapter = UserDatabaseAdapter(db=db)

    secret_password = await secretify(user.password)
    new_user = await adapter.create_one(
        user.model_dump() | {"secret_password": secret_password}
    )

    return User(**new_user.model_dump(exclude=["secret_password"]))
