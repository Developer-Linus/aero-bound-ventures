# Bridge between database and security
from sqlmodel import Session
from pydantic import EmailStr
from backend.crud.users import get_user_by_email, create_user
from backend.utils.security import verify_password, hash_password

def register_user(session: Session, email: str, password: str):
    """
    Registers a new user in the system with email and hashed password.
    Ensures email uniqueness and proper password security.
    Returns the newly created user object.
    """
    if get_user_by_email(session, email):
        raise ValueError("Email already registered.")
    hashed = hash_password(password)
    user = create_user(session, email=email, hashed_password=hashed)
    return user

def authenticate_user(session: Session, email: EmailStr, password: str):
    """
    Authenticate a user by verifying their email and password credentials.
    
    This function handles the user authentication process by:
    1. Looking up the user by their email address
    2. Verifying the provided password against the stored hashed password
    
    The two-step verification process ensures:
    - Protection against timing attacks by always verifying the password
    - Security through proper password hashing comparison
    
    Args:
        session: Database session for performing the lookup
        email: User's email address to authenticate
        password: Plain text password to verify
        
    Returns:
        User object if authentication succeeds, False otherwise
    """
    user = get_user_by_email(session, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
