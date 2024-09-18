import logging
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from backend.src.api.v1.function.jwt_function import (
    create_access_token,
    decrypt_access_token,
)
from backend.src.api.v1.function.pwd_hash import (
    get_password_hash,
    verify_password,
)
from backend.src.api.v1.shemas.base_model import Token, TokenData, CreateUser
from backend.db_orm.CRUD import UserCRUD

logging.basicConfig(level=logging.INFO)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

AuthRouter = APIRouter(tags=["API - V1"], prefix="/api/v1/auth")

user_crud = UserCRUD()


@AuthRouter.post("/register", response_model=Token)
async def register_user(user: CreateUser):
    user_exists = await user_crud.get_user_by_email(user.email)
    if user_exists:
        raise HTTPException(status_code=400, detail="User already registered")

    hashed_password = get_password_hash(user.password)
    new_user = await user_crud.create_user(
        tg_user_id=user.tg_user_id,
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
    )

    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@AuthRouter.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_crud.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@AuthRouter.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    email = await decrypt_access_token(token)
    user = await user_crud.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
