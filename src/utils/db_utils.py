from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.core.models import User, Board, Post

def get_user_from_db(user_email: str, db: Session):
    '''
    유저 검색 함수

    유저 이메일을 입력받아 DB에서 일치하는 유저 객체를 반환

        Arguements:
            user_email (str): 유저의 이메일
            db (Session): DB 세션

        Raises:
            HTTP_401_UNAUTHORIZED: 이메일이 일치하는 계정이 없는 경우

        Returns:
            유저 객체
    '''
    user = db.query(User).filter(User.email==user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='해당 이메일의 계정이 존재하지 않습니다.')
    return user

def get_board_from_db(board_id: int, db: Session):
    '''
    게시판 검색 함수

    게시판 id를 입력받아 DB에서 일치하는 게시판 객체를 반환

        Arguements:
            board_id (int): 게시판 ID
            db (Session): DB 세션

        Raises:
            HTTP_404_NOT_FOUND: 해당하는 게시판이 존재하지 않는 경우

        Returns:
            게시판 객체
    '''
    board = db.query(Board).get(board_id)
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시판을 찾을 수 없습니다.")
    return board

def get_post_from_db(post_id: int, db: Session):
    '''
    게시글 검색 함수

    게시글 id를 입력받아 DB에서 일치하는 게시판 객체를 반환

        Arguements:
            post_id (int): 게시글 ID
            db (Session): DB 세션

        Raises:
            HTTP_404_NOT_FOUND: 해당하는 게시글이 존재하지 않는 경우

        Returns:
            게시글 객체
    '''
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")
    return post