from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from backend.crud.database import get_session
from sqlmodel import Session
from backend.schemas.users import UserCreate, UserRead
from backend.services.auth import register_user, authenticate_user
from backend.utils.email import send_email
from backend.schemas.users import Token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from backend.utils.security import create_access_token

router = APIRouter()


@router.post("/register", response_model=UserRead, tags=["users"])
async def register(
    background_tasks: BackgroundTasks,
    user_in: UserCreate,
    session: Session = Depends(get_session),
):
    try:
        user = register_user(session, email=user_in.email, password=user_in.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    subject = "Welcome to Aero Bound Ventures"
    recipients = [user_in.email]
    body_text = f"Hello {user_in.email},\n\nWelcome to Aero Bound Ventures. We are excited to have you join our community."
    background_tasks.add_task(send_email, subject, recipients, body_text)
    return user
@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_session)) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
            data={"sub": user.email}
        )
    return Token(access_token=access_token, token_type="bearer")