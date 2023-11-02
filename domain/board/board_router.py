from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.board import board_schema
from models import Board

router = APIRouter(
    prefix="/board"
)


## 게시판 생성
@router.post("/create")
def board_create(created_board: board_schema.CreateBoard, db: Session = Depends(get_db)):
    _board = Board(
        name = created_board.name,
        public = created_board.public
    )
    db.add(_board)
    db.commit()
    return _board


## 게시판 수정
@router.put("/update")
def board_update(updated_board: board_schema.UpdateBoard, db: Session = Depends(get_db)):
    _board = db.query(Board).get(updated_board.id)
    if not _board:
        raise Exception("존재하지 않는 게시판 입니다.")
    _board.name = updated_board.name
    _board.public = updated_board.public

    db.commit()

    return _board.id


## 게시판 삭제
@router.delete("/delete/{board_id}")
def board_delete(board_id : int, db: Session = Depends(get_db)):
    _board = db.query(Board).get(board_id)
    if not _board:
        return {'msg': "존재하지 않는 게시판 입니다."}
    db.delete(_board)
    db.commit()
    return {'msg':'삭제되었습니다.'}


## 게시판 상세
@router.get("/get/{board_id}")
def board_detail(board_id : int, db: Session = Depends(get_db)):
    _board = db.query(Board).get(board_id)
    if not _board:
        return {'msg': "존재하지 않는 게시판 입니다."}
    
    return _board


## 게시판 목록
@router.get("/list")
def board_list(db: Session = Depends(get_db)):
    _board_list = db.query(Board).all()
    return _board_list