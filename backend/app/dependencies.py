from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import User
from app.security import validate_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session),
) -> User:
    try:
        subject = validate_token(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.get(User, subject)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
def _bearer_token_optional(authorization: str | None = Header(default=None)) -> str | None:
    if not authorization:
        return None
    scheme, param = get_authorization_scheme_param(authorization)
    if scheme.lower() != "bearer":
        return None
    return param or None


def get_current_user_optional(
    token: str | None = Depends(_bearer_token_optional),
    db: Session = Depends(get_session),
) -> User | None:
    if not token:
        return None
    try:
        subject = validate_token(token)
    except ValueError:
        return None
    return db.get(User, subject)
