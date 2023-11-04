from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.domain.board import board_schema
from src.core.models import Board

router = APIRouter(
    prefix="/board"
)


def board_name_validator(board_name: str, db: Session = Depends(get_db)):
    '''
    게시판 이름 중복 체크 함수

    입력받은 게시판 이름이 이미 사용되고 있는지 확인

        Arguments
            board_name (str): 입력받은 게시판의 이름
            db: DB 세션
        
        Returns
            True: 이미 같은 이름의 게시판이 존재하는 경우
            False: 같은 이름의 게시판이 존재하지 않는 경우
    '''
    if db.query(Board).filter_by(name=board_name).all():
        return True
    else:
        return False


@router.post("/create")
def board_create(created_board: board_schema.CreateBoard, db: Session = Depends(get_db)):
    '''
    게시판 생성 함수

    새로운 board 객체를 생성하고 DB에 저장

        Arguments
            CreateBoard (name, public): 게시판 생성 입력 Schema
            db: DB 세션

        Returns
            생성한 board 객체
        
        exceptions
            ValueError: 이미 존재하는 이름으로 게시판을 생성하려는 경우
    '''
    if board_name_validator(created_board.name, db):
        raise ValueError('같은 이름의 게시판이 이미 존재합니다.')
    _board = Board(
        name = created_board.name,
        public = created_board.public
    )
    db.add(_board)
    db.commit()
    return _board


@router.put("/update")
def board_update(updated_board: board_schema.UpdateBoard, db: Session = Depends(get_db)):
    '''
    게시판 수정 함수

    입력받은 id가 일치하는 게시판의 name과 public을 수정하고 DB 저장

        Arguments
            UpdatedBoard (id, name, public)
            db: DB 세션

        Returns
            수정한 board 객체의 id

        exceptions
            ValueError: 이미 존재하는 이름으로 게시판을 수정하려는 경우
    '''
    _board = db.query(Board).get(updated_board.id)
    if not _board:
        raise Exception("존재하지 않는 게시판 입니다.")
    if board_name_validator(updated_board.name, db):
        raise ValueError('같은 이름의 게시판이 이미 존재합니다.')
    _board.name = updated_board.name
    _board.public = updated_board.public
    db.commit()
    return _board.id


@router.delete("/delete/{board_id}")
def board_delete(board_id: int, db: Session = Depends(get_db)):
    '''
    게시판 삭제 함수

    게시판 id를 입력받아 해당 게시판을 DB에서 삭제

        Arguments
            board_id (int): 삭제할 게시판의 id
            db : DB 세션

        Returns
            삭제 완료 메시지

        Exceptions
            게시판 조회 불가 메시지: 입력한 id와 일치하는 게시판이 없는 경우

    '''
    _board = db.query(Board).get(board_id)
    if not _board:
        raise Exception("존재하지 않는 게시판 입니다.")
    db.delete(_board)
    db.commit()
    return {'msg':'삭제되었습니다.'}


@router.get("/get/{board_id}")
def board_detail(board_id : int, db: Session = Depends(get_db)):
    '''
    게시판 상세 조회 함수

    게시판 ID를 입력받아 해당 게시판을 조회

        Arguments
            board_id (int): 조회할 게시판의 id
            db: DB 세션

        Returns
            조회하는 게시판 객체

        Exceptions
            게시판 조회 불가 메시지: 입력한 id와 일치하는 게시판이 없는 경우
    '''
    _board = db.query(Board).get(board_id)
    if not _board:
        return {'msg': "존재하지 않는 게시판 입니다."}
    return _board


@router.get("/list")
def board_list(db: Session = Depends(get_db)):
    '''
    게시판 목록 조회 함수

    전체 게시판 목록을 조회

        Arguments
            db: DB 세션

        Returns
            전체 게시판 목록
    '''
    _board_list = db.query(Board).all()
    return _board_list