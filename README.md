# FastAPI-Blog

## Environment

- Python 3.11.6
- FastAPI 0.104.1
- SQLalchemy 2.0.22
- PostgreSQL 14.9

## Installation

```bash
$ git clone https://github.com/jjiisub/Elice-interview-project.git
$ cd Elice-interview-project
$ pip install -r requirements.txt
```

### .env File

```shell
## .env

ACCESS_TOKEN_EXPIRE_SECONDS=3600
SQLALCHEMY_DATABASE_URL="postgresql://DB_USER:PASSWORD@DB_URL/DB_NAME"
PAGE_SIZE=2
REDIS_HOST="REDIS_URL"
REDIS_PORT=6379
REDIS_DATABASE=0
```

### Database

```bash
$ alembic init migrations
```

```ini
## alembic.ini

...
sqlalchemy.url = postgresql://DB_USER:PASSWORD@DB_URL/DB_NAME
...
```

```python
## migrations/env.py

from src.core import models
...
target_metadata = models.Base.metadata
...
```

```bash
$ alembic revision --autogenerate
$ alembic upgrade head
```

### Backend

```bash
$ uvicorn main:app --reload
```

## Modules

- `src/utils/auth.py` : 유저 인증 및 권한 확인

- `src/utils/config.py` : .env 파일 세팅

- `src/utils/db_utils.py` : DB로부터 객체 조회 및 예외 처리

- `src/utils/validator.py` : 중복 예외 처리

## Issues

### User, Board 생성 시 transaction 충돌 문제

name validator를 통해 user와 board 생성 시 중복 여부를 확인한다. 이때 동일한 이름으로 동시에 생성하는 경우에는 validator로 중복 여부를 확인할 수 없고, DB commit 시 Server Error가 발생하게 된다.

이를 해결하기 위해 `try/except`를 이용하여 DB 상에서 충돌이 발생한 경우에는 중복된 이름이 이미 존재한다는 안내 문구를 반환하도록 구현하였다.

```python
## src/domain/board/board_router.py
try:
    db.add(_board)
    db.commit()
except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="같은 이름의 게시판이 이미 존재합니다.")

## src/domain/user/user_router.py
try:
    db.add(_user)
    db.commit()
except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="같은 이메일의 계정이 이미 존재합니다.")
```

### Board List 정렬 성능 최적화

`/board/list/` endpoint에서는 게시글 개수를 기준으로 정렬한 게시판 목록을 반환한다. 이때 매번 게시판의 게시글에 접근하는 반복 작업을 줄이기 위해 Board 모델에 post_count field를 추가하였다. 게시글을 생성 및 삭제할 때 매번 해당 게시판의 post_count field를 업데이트하도록 구현하였다.

```python
## src/core/models.py
class Board(Base):
    ...
    post_count = Column(Integer, default=0, nullable=False)
    ...

## src/domain/post/post_router.py
@router.post("/create/{board_id}")
def post_create(board_id: int,
    ...
    db.add(_post)
    _board.post_count += 1
    db.commit()
    ...
```

해당 column을 기준으로 인덱스를 생성하면 정렬된 게시판 목록 접근 성능을 높일 수 있다. 그러나 게시판의 생성 및 삭제가 자주 일어난다고 가정했을 때 인덱스의 수정이 반복되기 때문에 오히려 비효율적일 수 있다.

게시글 개수 카운트의 정확도를 높이기 위해서 접근한 게시판에 lock을 거는 방식으로 구현할 수 있다. SQLalchemy의 with_for_update()를 이용해서 row lock을 구현할 수 있다. 다른 transaction에서 lock을 걸어 놓은 상태이더라도 일정 기간동안 기다리기 때문에 순차적으로 진행될 수 있다. 그러나 게시글 생성, 삭제가 빈번하게 일어나는 게시판에서는 일정 기간 이후 drop되어 거부되는 요청이 많이 발생할 수 있다.
