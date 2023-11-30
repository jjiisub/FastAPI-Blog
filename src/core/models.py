from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.core.db_config import Base


class User(Base):
    '''
    User Model

        Attributes:
            id (int): primary key
            fullname (str): 유저 전체 이름
            email (str): 유저 이메일
            password (str): 유저 비밀번호
    '''
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


class Board(Base):
    '''
    Board Model (게시판)

        Attributes:
            id (int): primary key
            name (str): 게시판의 이름
            public (bool): 게시판 공개 여부 Flag
            user_id (int): 게시판을 생성한 유저의 ID
            post_count (int): 게시판의 게시글 수
            posts (list): 게시판의 게시글 목록
    '''
    __tablename__ = "board"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    public = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_count = Column(Integer, default=0, nullable=False)


class Post(Base):
    '''
    Post Model (게시글)

        Attributes:
            id (int): primary key
            board_id (int): foreign key, Board 객체의 ID
            title (str): 게시글의 제목
            content (str): 게시글의 내용
            user_id (int): 게시글을 생성한 유저의 ID
            board (Board): post가 작성된 board 객체
    '''
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    board_id = Column(Integer, ForeignKey("board.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    board = relationship("Board", backref="posts")