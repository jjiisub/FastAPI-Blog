from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from src.core.models import User, Board
from src.core.database import get_db

def board_name_validator(board_name: str, db: Session = Depends(get_db)):
    '''
    게시판 이름 중복 체크 함수

    입력받은 게시판 이름이 이미 DB에 존재하는지 확인

        Arguments:
            board_name (str): 게시판의 이름
            db: DB 세션
        
        Raises:
            HTTP_400_BAD_REQUEST: 같은 이름의 게시판이 이미 존재하는 경우

        Returns:
            None
    '''
    if db.query(Board).filter_by(name=board_name).all():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="같은 이름의 게시판이 이미 존재합니다.")
    return

def user_email_validator(email: str, db: Session):
    '''
    유저 이메일 중복 체크 함수

    입력받은 이메일이 이미 DB에 존재하는지 확인

        Arguments:
            email (str): 유저의 이메일
            db: DB 세션
        
        Raises:
            HTTP_400_BAD_REQUEST: 같은 이메일의 유저가 이미 존재하는 경우

        Returns:
            None
    '''
    _user = db.query(User).filter(User.email==email).first()
    if _user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="같은 이메일의 계정이 이미 존재합니다.")
    return