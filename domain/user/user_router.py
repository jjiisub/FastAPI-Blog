from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from domain.user import user_schema
from models import User

router = APIRouter(
    prefix="/user"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

## 회원가입
@router.post("/signup")
def user_create(created_user: user_schema.CreateUser, db: Session = Depends(get_db)):
    _user = User(
        email = created_user.email,
        fullname = created_user.fullname,
        password = pwd_context.hash(created_user.password1)
    )
    db.add(_user)
    db.commit()
    return _user