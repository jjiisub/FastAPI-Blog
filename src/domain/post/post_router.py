from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.utils.config import Settings
from src.utils.db_utils import get_post_from_db, get_board_from_db
from src.utils.auth import get_current_user, auth_post_edit, auth_board_read
from src.core.db_config import get_db
from src.core.models import Post, Board
from src.domain.post import post_schema

router = APIRouter(
    prefix="/post"
)


@router.post("/create/{board_id}")
def post_create(board_id: int,
                created_post: post_schema.Post,
                db: Session = Depends(get_db),
                curr_user_id: int = Depends(get_current_user)):
    '''
    게시글 생성 함수

    새로운 post 객체를 생성하고 DB에 저장, board 객체에 게시글 counting

        Arguements:
            board_id (int): 게시글을 작성할 게시판 ID
            created_post (Post): 게시글 입력 Schema
            db (Session): DB 세션
            curr_user_id (int): 현재 로그인된 유저 ID

        Raises:
            HTTP_401_UNAUTHORIZED: 해당 게시판에 게시글 작성 권한이 없는 경우
            HTTP_404_NOT_FOUND: 해당 게시판이 존재하지 않는 경우

        Returns:
            게시글 생성 완료 메시지
    '''
    _board = get_board_from_db(board_id, db)
    auth_board_read(_board, curr_user_id)
    _post = Post(
        board_id = board_id,
        title = created_post.title,
        content = created_post.content,
        user_id = curr_user_id
    )
    db.add(_post)
    _board.post_count += 1
    db.commit()
    return {'msg': '게시글이 생성되었습니다.'}


@router.patch("/update/{post_id}")
def post_update(post_id: int,
                updated_post: post_schema.Post,
                db: Session = Depends(get_db),
                curr_user_id: int = Depends(get_current_user)):
    '''
    게시글 수정 함수

    입력받은 id가 일치하는 게시글의 title과 content를 수정하고 DB 저장

        Arguements:
            post_id (int): 수정할 게시글 ID
            updated_post (Post): 게시글 입력 Schema
            db (Session): DB 세션
            curr_user_id (int): 현재 로그인된 유저 ID

        Raises:
            HTTP_401_UNAUTHORIZED: 해당 게시글 수정 권한이 없는 경우
            HTTP_404_NOT_FOUND: 해당 게시글이 존재하지 않는 경우


        Returns:
            게시글 수정 완료 메시지
    '''
    _post = get_post_from_db(post_id, db)
    auth_post_edit(_post, curr_user_id)
    _post.title = updated_post.title
    _post.content = updated_post.content
    db.commit()
    return {'msg': '게시글이 수정되었습니다.'}


@router.delete("/delete/{post_id}")
def post_delete(post_id : int,
                db: Session = Depends(get_db),
                curr_user_id: int = Depends(get_current_user)):
    '''
    게시글 삭제 함수

    게시글 id를 입력받아 해당 게시글을 DB에서 삭제, 게시판의 post count 수정

        Arguements:
            post_id (int): 삭제할 게시글의 ID
            db (Session): DB 세션
            curr_user_id (int): 현재 로그인된 유저 ID

        Raises:
            HTTP_401_UNAUTHORIZED: 해당 게시글 삭제 권한이 없는 경우
            HTTP_404_NOT_FOUND: 해당 게시글이 존재하지 않는 경우
            HTTP_404_NOT_FOUND: 게시글이 작성된 게시판이 존재하지 않는 경우

        Returns:
            삭제 완료 메시지
    '''
    _post = get_post_from_db(post_id, db)
    auth_post_edit(_post, curr_user_id)
    _board = get_board_from_db(_post.board_id, db)
    _board.post_count -= 1
    db.delete(_post)
    db.commit()
    return {'msg':'삭제되었습니다.'}


@router.get("/get/{post_id}")
def post_detail(post_id : int,
                db: Session = Depends(get_db),
                curr_user_id: int = Depends(get_current_user)):
    '''
    게시글 상세 조회 함수

    게시글 ID를 입력받아 해당 게시글을 조회

        Arguements:
            post_id (int): 조회할 게시글의 ID
            db (Session): DB 세션
            curr_user_id (int): 현재 로그인된 유저 ID

        Raises:
            HTTP_401_UNAUTHORIZED: 해당 게시글 조회 권한이 없는 경우
            HTTP_404_NOT_FOUND: 해당 게시글이 존재하지 않는 경우

        Returns:
            조회하는 게시글 객체
    '''
    _post = get_post_from_db(post_id, db)
    auth_board_read(_post.board, curr_user_id)
    return _post


@router.get("/list/{board_id}/{page}")
def post_list(board_id: int,
              db: Session = Depends(get_db),
              curr_user_id: int = Depends(get_current_user),
              page: int = 0):
    '''
    게시글 목록 조회 함수

    전체 게시글 목록을 조회

        Arguements:
            board_id (int): 조회하려는 게시판 ID
            db (Session): DB 세션
            curr_user_id (int): 현재 로그인된 유저 ID
            page (int): 조회하려는 게시글 목록의 페이지

        Raises:
            HTTP_401_UNAUTHORIZED: 해당 게시판 조회 권한이 없는 경우
            HTTP_404_NOT_FOUND: 해당 게시판이 존재하지 않는 경우

        Returns:
            post_count (int): 전체 게시글 수
            post_list (list): 해당 페이지의 게시글 목록
    '''
    _board = get_board_from_db(board_id, db)
    auth_board_read(_board, curr_user_id)
    _post_list = db.query(Board).get(board_id).posts
    size = Settings().PAGE_SIZE
    return {
        "post_count": len(_post_list),
        "post_list": _post_list[page*size:page*size+size]
    }