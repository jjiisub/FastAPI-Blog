from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Board(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    public = Column(Boolean, nullable=False)
    posts = relationship("Post", backref="board")

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    board_id = Column(Integer, ForeignKey("board.id"))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)