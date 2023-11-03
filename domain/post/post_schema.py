from pydantic import BaseModel, validator


class Post(BaseModel):
    '''
    게시글 수정 입력 Schema

        Attributes
            id (int): 생성할 게시글의 게시판 id 또는 수정할 게시글의 id
            title (str): 게시글의 제목
            content (str): 게시글의 내용

        Exceptions
            ValueError: 빈칸 또는 공백 문자만 입력된 경우
    '''
    id: int
    title: str
    content: str

    @validator('id', 'title', 'content')
    def not_null(cls, v):
        '''입력된 field에 빈칸 또는 공백 여부 체크'''
        if not v or ( type(v)==str and not v.strip() ):
            raise ValueError('빈 칸을 모두 채워주세요')
        return v