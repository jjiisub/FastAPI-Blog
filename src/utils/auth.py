from typing import Annotated

from fastapi import Depends, status, HTTPException

from src.core.models import Board, Post
from src.core.redis_config import get_redis
from src.domain.user.user_router import oauth2_scheme


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    '''
    현재 유저 정보 조회 함수

    인증 token으로 redis 로그인 세션을 조회하여 일치하는 유저의 id를 반환
        Attributes:
                token (str): 현재 로그인되어 있는 access token
            
        Raises:
            HTTP_401_UNAUTHORIZED: token이 redis에 저장되어 있지 않는 경우
        
        Returns:
            user_id (int): 현재 token에 해당하는 유저 ID
    '''
    rd = get_redis()
    user_id = rd.get(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='로그인이 필요합니다.')
    return int(user_id)

def auth_board_edit(board: Board, user_id: int):
    '''
    게시판 수정 권한 확인 함수

    현재 유저가 게시판을 생성한 유저인지 (수정 권한이 있는지) 확인

        Attributes:
                board (Board): 권한을 확인하려는 게시판 객체
                user_id (int): 현재 유저의 ID
            
        Raises:
            HTTP_401_UNAUTHORIZED: 해당 게시판에 대한 수정 권한이 없는 경우
        
        Returns:
            None
    '''
    if board.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="해당 게시판에 대한 수정 권한이 없습니다.")
    return

def auth_board_read(board: Board, user_id: int):
    '''
    게시판 접근 권한 확인 함수

    현재 유저가 게시판 정보 조회 및 게시글 조회 권한이 있는지 확인

        Attributes:
                board (Board): 권한을 확인하려는 게시판 객체
                user_id (int): 현재 유저의 ID
            
        Raises:
            HTTP_401_UNAUTHORIZED: 해당 게시판에 대한 접근 권한이 없는 경우
        
        Returns:
            None
    '''
    if not board.public and board.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="해당 게시판에 대한 접근 권한이 없습니다.")
    return

def auth_post_edit(post: Post, user_id: int):
    '''
    게시글 수정 권한 확인 함수

    현재 유저가 게시글을 작성한 유저인지 (수정 권한이 있는지) 확인

        Attributes:
                post (Post): 권한을 확인하려는 게시판 객체
                user_id (int): 현재 유저의 ID
            
        Raises:
            HTTP_401_UNAUTHORIZED: 해당 게시글에 대한 수정 권한이 없는 경우
        
        Returns:
            None
    '''
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="해당 게시글에 대한 수정 권한이 없습니다.")
    return