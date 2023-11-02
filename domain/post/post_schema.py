from pydantic import BaseModel


class CreatePost(BaseModel):
    board_id: int
    title: str
    content: str


class UpdatePost(BaseModel):
    id: int
    title: str
    content: str

class RetrievePost(BaseModel):
    id: int
