from pydantic import EmailStr
from sqlmodel import SQLModel, Field
import uuid


class UserInDB(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str
