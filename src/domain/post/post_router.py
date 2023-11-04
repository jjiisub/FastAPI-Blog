from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.domain.post import post_schema
from src.core.models import Post

router = APIRouter(
    prefix="/post"
)


@router.post("/create")
def post_create(created_post: post_schema.Post, db: Session = Depends(get_db)):
    '''
    게시글 생성 함수

    새로운 board 객체를 생성하고 DB에 저장

        Arguements:
            CreatePost (board_id, title, content): 게시글 생성 입력 Schema
            db: DB 세션

        Returns:
            생성한 post 객체
    '''
    _post = Post(
        board_id = created_post.board_id,
        title = created_post.title,
        content = created_post.content
    )
    db.add(_post)
    db.commit()
    return _post


@router.put("/update")
def post_update(updated_post: post_schema.Post, db: Session = Depends(get_db)):
    '''
    게시글 수정 함수

    입력받은 id가 일치하는 게시글의 title과 content를 수정하고 DB 저장

        Arguements:
            UpdatedPost (id, title, content)
            db: DB 세션

        Returns:
            수정한 post 객체
    '''
    _post = db.query(Post).get(updated_post.id)
    if not _post:
        return {'msg': '존재하지 않는 게시글입니다.'}
    _post.title = updated_post.title
    _post.content = updated_post.content
    db.commit()
    return _post


@router.delete("/delete/{post_id}")
def post_delete(post_id : int, db: Session = Depends(get_db)):
    '''
    게시글 삭제 함수

    게시글 id를 입력받아 해당 게시글을 DB에서 삭제

        Arguements:
            post_id (int): 삭제할 게시글의 id
            db : DB 세션

        Returns:
            삭제 완료 메시지

        Exceptions:
            게시글 조회 불가 메시지: 입력한 id와 일치하는 게시글이 없는 경우

    '''
    _post = db.query(Post).get(post_id)
    if not _post:
        return {'msg': "존재하지 않는 게시글입니다."}
    db.delete(_post)
    db.commit()
    return {'msg':'삭제되었습니다.'}


## 게시글 상세
@router.get("/get/{post_id}")
def post_detail(post_id : int, db: Session = Depends(get_db)):
    '''
    게시글 상세 조회 함수

    게시글 ID를 입력받아 해당 게시글을 조회

        Arguements:
            post_id (int): 조회할 게시글의 id
            db: DB 세션

        Returns:
            조회하는 게시글 객체

        Exceptions:
            게시글 조회 불가 메시지: 입력한 id와 일치하는 게시글이 없는 경우
    '''
    _post = db.query(Post).get(post_id)
    if not _post:
        return {'msg': "존재하지 않는 게시글입니다."}
    return _post


@router.get("/list")
def post_list(db: Session = Depends(get_db)):
    '''
    게시글 목록 조회 함수

    전체 게시글 목록을 조회

        Arguements:
            db: DB 세션

        Returns:
            전체 게시글 목록
    '''
    _post_list = db.query(Post).all()
    return _post_list