# backend/app/services/auth_service.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.app.config import settings
from backend.app import models, schemas
from sqlalchemy.orm import Session

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret keys
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


# -------------------
# Password Handling
# -------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# -------------------
# JWT Token Handling
# -------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# -------------------
# User Authentication
# -------------------
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


def register_user(db: Session, user_data: schemas.UserCreate):
    hashed_pw = hash_password(user_data.password)
    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
