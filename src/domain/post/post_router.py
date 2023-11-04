from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.utils.config import get_settings
from src.core.database import get_db
from src.core.models import Post, User, Board
from src.domain.post import post_schema
from src.domain.user.user_router import get_current_user

router = APIRouter(
    prefix="/post"
)


@router.post("/create")
def post_create(created_post: post_schema.Post,
                db: Session = Depends(get_db),
                curr_user_id: int = Depends(get_current_user)):
    '''
    게시글 생성 함수

    새로운 board 객체를 생성하고 DB에 저장

        Arguements
            CreatePost (board_id, title, content): 게시글 생성 입력 Schema
            db: DB 세션

        Returns
            생성한 post 객체
    '''
    board = db.query(Board).get(created_post.id)
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not board.public and board.user_id != curr_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    _post = Post(
        board_id = created_post.id,
        title = created_post.title,
        content = created_post.content,
        user_id = curr_user_id
    )
    db.add(_post)
    board.post_count += 1
    db.commit()
    return _post


@router.put("/update")
def post_update(updated_post: post_schema.Post,
                db: Session = Depends(get_db),
                curr_user_id: int = Depends(get_current_user)):
    '''
    게시글 수정 함수

    입력받은 id가 일치하는 게시글의 title과 content를 수정하고 DB 저장

        Arguements
            UpdatedPost (id, title, content)
            db: DB 세션

        Returns
            수정한 post 객체
    '''
    if _post.user_id != curr_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    _post = db.query(Post).get(updated_post.id)
    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    _post.title = updated_post.title
    _post.content = updated_post.content
    db.commit()
    return _post


@router.delete("/delete/{post_id}")
def post_delete(post_id : int,
                db: Session = Depends(get_db),
                curr_user_id: int = Depends(get_current_user)):
    '''
    게시글 삭제 함수

    게시글 id를 입력받아 해당 게시글을 DB에서 삭제

        Arguements
            post_id (int): 삭제할 게시글의 id
            db : DB 세션

        Returns
            삭제 완료 메시지

        Exceptions
            게시글 조회 불가 메시지: 입력한 id와 일치하는 게시글이 없는 경우

    '''
    if _post.user_id != curr_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    _post = db.query(Post).get(post_id)
    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(_post)
    db.commit()
    return {'msg':'삭제되었습니다.'}


## 게시글 상세
@router.get("/get/{post_id}")
def post_detail(post_id : int,
                db: Session = Depends(get_db),
                curr_user_id: int = Depends(get_current_user)):
    '''
    게시글 상세 조회 함수

    게시글 ID를 입력받아 해당 게시글을 조회

        Arguements
            post_id (int): 조회할 게시글의 id
            db: DB 세션

        Returns
            조회하는 게시글 객체

        Exceptions
            게시글 조회 불가 메시지: 입력한 id와 일치하는 게시글이 없는 경우
    '''
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not post.board.public and post.board.user_id != curr_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return post


@router.get("/list/{board_id}/{page}")
def post_list(board_id: int,
              db: Session = Depends(get_db),
              curr_user_id: int = Depends(get_current_user),
              page: int = 0):
    '''
    게시글 목록 조회 함수

    전체 게시글 목록을 조회

        Arguements
            db: DB 세션

        Returns
            전체 게시글 목록
    '''
    board = db.query(Board).get(board_id)
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not board.public and board.user_id != curr_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    _post_list = db.query(Board).get(board_id).posts

    settings = get_settings()
    size = settings.PAGE_SIZE
    return {
        "post_count": len(_post_list),
        "post_list": _post_list[page*size:page*size+size]
    }
    return _post_list