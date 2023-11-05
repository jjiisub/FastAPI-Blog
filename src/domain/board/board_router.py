from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from src.utils.config import Settings
from src.core.models import Board
from src.core.db_config import get_db
from src.domain.board import board_schema
# from src.domain.user.user_router import get_current_user
from src.utils.auth import get_current_user
from src.utils.validator import board_name_validator
from src.utils.db_utils import get_board_from_db

router = APIRouter(
    prefix="/board"
)


@router.post("/create")
def board_create(created_board: board_schema.Board,
                 db: Session = Depends(get_db),
                 curr_user_id: int = Depends(get_current_user)):
    '''
    게시판 생성 함수

    새로운 board 객체를 생성하고 DB에 저장

        Arguments:
            created_board (Board): 게시판 Schema
            db (Session): DB 세션

        Raises:
            HTTP_400_BAD_REQUEST: 이미 존재하는 이름으로 게시판을 생성하려는 경우

        Returns:
            board 생성 완료 메시지
    '''
    board_name_validator(created_board.name, db)
    _board = Board(
        name = created_board.name,
        public = created_board.public,
        user_id = curr_user_id
    )
    db.add(_board)
    db.commit()
    return {'msg': '게시판 생성이 완료되었습니다.'}


@router.patch("/update/{board_id}")
def board_update(board_id: int,
                 updated_board: board_schema.Board,
                 db: Session = Depends(get_db),
                 curr_user_id: int = Depends(get_current_user)):
    '''
    게시판 수정 함수

    입력받은 id가 일치하는 게시판의 name과 public을 수정하고 DB 저장

        Arguments:
            board_id (int): 수정하려는 게시판 ID
            updated_board (Board): 게시판 Schema
            db (Session): DB 세션
            curr_user_id (int): 현재 로그인된 유저 ID

        Raises:
            HTTP_400_BAD_REQUEST: 해당하는 게시판이 존재하지 않는 경우
            HTTP_401_UNAUTHORIZED: 해당 게시판의 수정 권한이 없는 경우
            HTTP_404_NOT_FOUND: 이미 존재하는 이름으로 게시판을 수정하려는 경우

        Returns:
            게시판 수정 완료 메시지
    '''
    _board = get_board_from_db(board_id, db)
    if _board.user_id != curr_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="자신이 생성한 게시판만 수정할 수 있습니다.")
    board_name_validator(updated_board.name, db)
    _board.name = updated_board.name
    _board.public = updated_board.public
    db.commit()
    return {'msg': '게시판 수정이 완료되었습니다.'}


@router.delete("/delete/{board_id}")
def board_delete(board_id: int,
                 db: Session = Depends(get_db),
                 curr_user_id: int = Depends(get_current_user)):
    '''
    게시판 삭제 함수

    게시판 id를 입력받아 해당 게시판을 DB에서 삭제

        Arguments:
            board_id (int): 삭제할 게시판의 ID
            db (Session): DB 세션
            curr_user_id (int): 현재 로그인된 유저 ID

        Raises:
            HTTP_401_UNAUTHORIZED: 해당 게시판의 삭제 권한이 없는 경우
            HTTP_404_NOT_FOUND: 입력한 ID와 일치하는 게시판이 없는 경우

        Returns:
            게시판 삭제 완료 메시지
    '''
    _board = get_board_from_db(board_id, db)
    if _board.user_id != curr_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="자신이 생성한 게시판만 수정할 수 있습니다.")
    db.delete(_board)
    db.commit()
    return {'msg':'삭제되었습니다.'}


@router.get("/get/{board_id}")
def board_detail(board_id : int,
                 db: Session = Depends(get_db),
                 curr_user_id: int = Depends(get_current_user)):
    '''
    게시판 상세 조회 함수

    게시판 ID를 입력받아 해당 게시판을 조회

        Arguments:
            board_id (int): 조회할 게시판의 ID
            db (Session): DB 세션
            curr_user_id (int): 현재 로그인된 유저 ID

        Raises:
            HTTP_401_UNAUTHORIZED: 해당 게시판의 조회 권한이 없는 경우
            HTTP_404_NOT_FOUND: 입력한 id와 일치하는 게시판이 없는 경우

        Returns:
            조회하는 게시판 객체
    '''
    _board = get_board_from_db(board_id, db)
    if not _board.public and _board.user_id != curr_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="게시판 조회 권한이 없습니다.")
    return _board


@router.get("/list/{page}")
def board_list(db: Session = Depends(get_db),
               curr_user_id: int = Depends(get_current_user),
               page: int = 0):
    '''
    게시판 목록 조회 함수

    전체 게시판 목록을 조회

        Arguments:
            db (Session): DB 세션
            curr_user_id (int): 현재 로그인된 유저 ID
            page (int): 조회하려는 게시판 목록의 페이지

        Returns:
            전체 게시판 목록의 해당 페이지
    '''
    size = Settings().PAGE_SIZE

    _board_list = db.query(Board).filter((Board.user_id == curr_user_id) | (Board.public)).order_by(Board.post_count.desc())
    total = _board_list.count()
    board_list_paged = _board_list.offset(page*size).limit(size).all()

    return {
        "board_count": total,
        "board_list": board_list_paged
    }