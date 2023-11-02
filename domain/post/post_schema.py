from pydantic import BaseModel


class CreatePost(BaseModel):
    '''
    게시글 생성 입력 Schema

        Attributes
            board_id (int): 생성할 게시글의 게시판의 id
            title (str): 생성할 게시글의 제목
            content (str): 생성할 게시글의 내용
    '''
    board_id: int
    title: str
    content: str


class UpdatePost(BaseModel):
    '''
    게시글 수정 입력 Schema

        Attributes
            id (int): 수정할 게시글의 id
            title (str): 변경된 게시글의 제목
            content (str): 변경된 게시글의 내용
    '''
    id: int
    title: str
    content: str

# class RetrievePost(BaseModel):
#     id: int
