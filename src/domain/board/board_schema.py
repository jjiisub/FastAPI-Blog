from pydantic import BaseModel, validator
from fastapi import status, HTTPException

class Board(BaseModel):
    '''
    게시판 생성 입력 Schema

        Attributes:
            name (str): 생성할 게시판의 이름
            public (str): 게시판 공개 여부 Flag
        
        Raises:
            HTTP_400_BAD_REQUEST: 빈칸 또는 공백 문자만 입력된 경우
    '''
    name: str
    public: bool

    @validator('name', 'public')
    def not_null(cls, v):
        '''
        각 field가 빈칸 또는 공백 문자인지 체크
        '''
        if type(v) == str and (not v or not v.strip()):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="빈 칸을 모두 채워주세요")
        if type(v) == bool and v == None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="빈 칸을 모두 채워주세요")
        return v


# class UpdateBoard(BaseModel):
#     '''
#     게시판 수정 입력 Schema

#         Attributes
#             id (int): 수정할 게시판의 id
#             name (str): 변경될 게시판 이름
#             public (bool): 변경될 공개 여부 Flag
        
#         Exceptions
#             ValueError: 빈칸 또는 공백 문자만 입력된 경우
#     '''
#     id: int
#     name: str
#     public: bool

#     @validator('id', 'name')
#     def not_null(cls, v):
#         '''입력된 field에 빈칸 또는 공백 문자 체크'''
#         if not v or ( type(v)==str and not v.strip() ):
#             raise ValueError('빈 칸을 모두 채워주세요')
#         return v
    
#     @validator('public')
#     def not_null_bool(cls, v):
#         '''Boolean field의 null 체크'''
#         if v == None:
#             raise ValueError('빈 칸을 모두 채워주세요')
#         return v