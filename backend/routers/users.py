from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from backend.crud.database import get_session
from sqlmodel import Session
from backend.schemas.users import UserCreate, UserRead
from backend.crud.users import get_user_by_email, create_user
from backend.utils.email import send_email

router = APIRouter()


@router.post("/register", response_model=UserRead, tags=["users"])
async def register(
    background_tasks: BackgroundTasks,
    user_in: UserCreate,
    session: Session = Depends(get_session),
):
    user = get_user_by_email(session, user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered."
        )
    user = create_user(session, email=user_in.email, password=user_in.password)
    subject = "Welcome to Aero Bound Ventures"
    recipients = [user_in.email]
    body_text = f"Hello {user_in.email},\n\nWelcome to Aero Bound Ventures. We are excited to have you join our community."
    background_tasks.add_task(send_email, subject, recipients, body_text)
    return user
