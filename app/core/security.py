from datetime import datetime, timedelta, timezone
from typing import Optional, Dict


from jose import jwt, JWTError
import hashlib
from passlib.context import CryptContext

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlmodel import Session, select

from app.core.config import settings
from app.database import get_db
from app.models.admin import Admin

# ===================================
# CONFIG JWT
# ===================================

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# ===================================
# HASH MOT DE PASSE
# ===================================


pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
# OAUTH2

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")


# ADMIN DB

def get_admin_by_username(db: Session, username: str) -> Optional[Admin]:
    return db.exec(
        select(Admin).where(Admin.username == username)
    ).first()

def authenticate_admin(db: Session, username: str, password: str) -> Optional[Admin]:
    admin = get_admin_by_username(db, username)
    if not admin:
        return None
    if not verify_password(password, admin.hashed_password):
        return None
    return admin


# JWT

def create_access_token(
    data: Dict[str, str],
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc) + expires_delta
        if expires_delta
        else datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Dict[str, str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {"username": username}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )


# DEPENDANCE FASTAPI (PROTECTION ADMIN)

def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Admin:
    token_data = verify_token(token)

    admin = get_admin_by_username(db, token_data["username"])

    if not admin or not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin inactif ou non autorisé",
        )

    return admin
