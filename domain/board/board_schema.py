from pydantic import BaseModel


class CreateBoard(BaseModel):
    '''
    게시판 생성 입력 Schema

        Attributes
            name (str): 생성할 게시판의 이름
            public (str): 게시판 공개 여부 Flag
    '''
    name: str
    public: bool


class UpdateBoard(BaseModel):
    '''
    게시판 수정 입력 Schema

        Attributes
            id (int): 수정할 게시판의 id
            name (str): 변경될 게시판 이름
            public (bool): 변경될 공개 여부 Flag
    '''
    id: int
    name: str
    public: bool


# class RetrieveBoard(BaseModel):
#     '''
#     게시판 
#     '''
#     id: int