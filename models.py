from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    '''
    User Model

        Attributes
            id (int): primary key

            fullname (str)

            email (str)

            password (str)
    '''
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


class Board(Base):
    '''
    Board Model (게시판)

        Attributes
            id (int): primary key

            name (str)
            
            public (bool): 게시판 공개 여부 Flag
            
            posts (list): 해당 게시판에 속한 게시글 목록
    '''
    __tablename__ = "board"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    public = Column(Boolean, nullable=False)
    posts = relationship("Post", backref="board")


class Post(Base):
    '''
    Post Model (게시글)

        Attributes
            id (int): primary key

            board_id (int): foreign key, Board 객체의 id

            title (str)

            content (str)
    '''
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    board_id = Column(Integer, ForeignKey("board.id"))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)