from pydantic import BaseModel, validator
from fastapi import status, HTTPException


class Post(BaseModel):
    '''
    게시글 수정 입력 Schema

        Attributes:
            title (str): 게시글의 제목
            content (str): 게시글의 내용

        Raises:
            HTTP_400_BAD_REQUEST: 빈칸 또는 공백 문자만 입력된 경우
    '''
    title: str
    content: str

    @validator('title', 'content')
    def not_null(cls, v):
        '''
        입력된 field에 빈칸 또는 공백 여부 체크
        '''
        if not v or ( type(v)==str and not v.strip() ):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="빈 칸을 모두 채워주세요")
        return v