# Elice Backend Interview Project

## Environment

- Python 3.11.6
- FastAPI 0.104.1
- PostgreSQL 14.9

## Installation

```
$ git clone https://github.com/jjiisub/Elice-interview-project.git
$ cd Elice-interview-project
$ pip install -r requirements.txt
```

### .env File

```
ACCESS_TOKEN_EXPIRE_SECONDS=3600
SQLALCHEMY_DATABASE_URL="postgresql://DB_USER:PASSWORD@DB_URL/DB_NAME"
PAGE_SIZE=2
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
## /migrations/env.py

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

## Docstring

```python
def foo():
    '''
    Function Description

        Arguements:
            a (int): integer

        Returns:
            b (bool): boolean
    '''
    return

class poo():
    '''
    Class Description

        Attributes:
            ...

        Methods:
            ...
    '''
```
