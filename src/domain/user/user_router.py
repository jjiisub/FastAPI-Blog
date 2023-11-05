from typing import Annotated
import secrets

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src.core.models import User
from src.core.database import get_db
from src.domain.user import user_schema
from src.core.redis_config import get_redis
from src.utils.config import Settings

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="같은 이메일의 계정이 이미 존재합니다.")
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='이메일 또는 비밀번호가 잘못되었습니다.')
    access_token = secrets.token_hex(32)
    rd = get_redis()
    rd.set(access_token, user.id)
    rd.expire(access_token, Settings().ACCESS_TOKEN_EXPIRE_SECONDS)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_email": user.email
    }

# @router.get("/curr_user")
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    rd = get_redis()
    user_id = rd.get(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='로그인이 필요합니다.')
    return int(user_id)

@router.post("/logout")
def logout(token: Annotated[str, Depends(oauth2_scheme)]):
    rd = get_redis()
    rd.delete(token)
    return {"msg":"정상적으로 로그아웃되었습니다."}