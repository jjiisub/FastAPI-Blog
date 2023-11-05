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
from src.utils.validator import user_email_validator

router = APIRouter(
    prefix="/user"
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(email: str, db: Session):
    return db.query(User).filter(User.email==email).first()


@router.post("/signup")
def user_create(created_user: user_schema.CreateUser, db: Session = Depends(get_db)):
    '''
    유저 생성 (회원가입) 함수

    새로운 유저를 생성하고 DB에 저장

        Arguements:
            created_user (CreateUser): 유저 생성 입력 Schema
            db: DB 세션

        Raises:
            HTTP_400_BAD_REQUEST: 같은 이메일 계정이 이미 있는 경우

        Returns:
            회원가입 완료 메시지
    '''
    user_email_validator(created_user.email, db)
    _user = User(
        email = created_user.email,
        fullname = created_user.fullname,
        password = pwd_context.hash(created_user.password1)
    )
    db.add(_user)
    db.commit()
    return {'msg': '회원가입이 완료되었습니다.'}


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    '''
    유저 로그인 함수

    입력받은 유저 정보를 검증한 후 redis에 저장

        Arguements:
            form (OAuth2PasswordRequestForm): 유저 로그인 form
            db: DB 세션

        Returns:
            access_token: 권한 인증 access token
            token_type: Bearer
            user_email: 로그인한 유저의 이메일
    '''
    user = get_user(form.username, db)
    # user_email_validator(created_user.email, db)
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

# def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     rd = get_redis()
#     user_id = rd.get(token)
#     if not user_id:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='로그인이 필요합니다.')
#     return int(user_id)

@router.post("/logout")
def logout(token: Annotated[str, Depends(oauth2_scheme)]):
    '''
    유저 로그아웃 함수

    입력받은 access token을 redis에서 삭제

        Arguements:
                token (str): 현재 로그인되어 있는 access token 

        Returns:
            로그아웃 완료 메시지
    '''
    rd = get_redis()
    rd.delete(token)
    return {"msg":"정상적으로 로그아웃되었습니다."}