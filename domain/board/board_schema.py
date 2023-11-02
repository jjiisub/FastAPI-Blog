from pydantic import BaseModel


class CreateBoard(BaseModel):
    name: str
    public: bool


class UpdateBoard(BaseModel):
    id: int
    name: str
    public: bool


class RetrieveBoard(BaseModel):
    id: int