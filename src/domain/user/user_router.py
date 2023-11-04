from typing import Annotated
import secrets

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src.core.models import User
from src.core.database import get_db
from src.domain.user import user_schema
from src.core.redis_config import get_redis
from src.utils.config import Settings, get_settings

# ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')

router = APIRouter(
    prefix="/user"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(email: str, db: Session):
    return db.query(User).filter(User.email==email).first()


@router.post("/signup")
def user_create(created_user: user_schema.CreateUser, db: Session = Depends(get_db)):
    user = get_user(created_user.email, db)
    if user:
        raise ValueError('같은 이메일의 계정이 이미 존재합니다.')
    _user = User(
        email = created_user.email,
        fullname = created_user.fullname,
        password = pwd_context.hash(created_user.password1)
    )
    db.add(_user)
    db.commit()
    return _user


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(form.username, db)
    if not user or not pwd_context.verify(form.password, user.password):
        raise ValueError('이메일 또는 비밀번호가 잘못되었습니다.')
    
    settings = get_settings()
    access_token = secrets.token_hex(32)
    rd = get_redis()
    rd.set(access_token, user.id)
    rd.expire(access_token, settings.ACCESS_TOKEN_EXPIRE_SECONDS)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_email": user.email
    }

# @router.get("/curr_user")
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    rd = get_redis()
    user_id = int(rd.get(token))
    return user_id

@router.post("/logout")
def logout(token: Annotated[str, Depends(oauth2_scheme)]):
    rd = get_redis()
    rd.delete(token)
    return {"msg":"정상적으로 로그아웃되었습니다."}