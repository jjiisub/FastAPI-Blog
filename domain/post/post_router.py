from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.post import post_schema
from models import Post

router = APIRouter(
    prefix="/post"
)

## 게시글 생성
@router.post("/create")
def post_create(created_post: post_schema.CreatePost, db: Session = Depends(get_db)):
    _post = Post(
        board_id = created_post.board_id,
        title = created_post.title,
        content = created_post.content
    )
    db.add(_post)
    db.commit()
    return _post


## 게시글 수정
@router.put("/update")
def post_update(updated_post: post_schema.UpdatePost, db: Session = Depends(get_db)):
    _post = db.query(Post).get(updated_post.id)
    if not _post:
        return {'msg': '존재하지 않는 게시글입니다.'}
    _post.title = updated_post.title
    _post.content = updated_post.content
    db.commit()
    return _post


## 게시글 삭제
@router.delete("/delete/{post_id}")
def post_delete(post_id : int, db: Session = Depends(get_db)):
    _post = db.query(Post).get(post_id)
    if not _post:
        return {'msg': "존재하지 않는 게시글 입니다."}
    db.delete(_post)
    db.commit()
    return {'msg':'삭제되었습니다.'}


## 게시글 상세
@router.get("/get/{post_id}")
def post_detail(post_id : int, db: Session = Depends(get_db)):
    _post = db.query(Post).get(post_id)
    if not _post:
        return {'msg': "존재하지 않는 게시판 입니다."}
    return _post


## 게시글 목록
@router.get("/list")
def post_list(db: Session = Depends(get_db)):
    _post_list = db.query(Post).all()
    return _post_list