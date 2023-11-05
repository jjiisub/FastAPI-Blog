from fastapi import status, HTTPException
from pydantic import BaseModel, validator, EmailStr

class CreateUser(BaseModel):
    '''
    유저 생성 (회원가입) 입력 Schema

        Attributes:
            email (EmailStr): 유저 이메일
            fullname (str): 유저 풀네임
            password1 (str): 유저 비밀번호
            password2 (str): 유저 비밀번호 확인
        
        Raises:
            HTTP_400_BAD_REQUEST: 빈칸 또는 공백 문자만 입력된 경우
            HTTP_400_BAD_REQUEST: 입력한 두 번의 비밀번호가 일치하지 않는 경우
    '''
    email: EmailStr
    fullname: str
    password1: str
    password2: str

    @validator('email','fullname','password1','password2')
    def not_empty(cls, v):
        '''
        각 field가 빈칸 또는 공백 문자인지 체크
        '''
        if not v or not v.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="빈 칸을 모두 채워주세요")
        return v
    
    @validator('password2')
    def password_check(cls, v, values):
        '''
        비밀번호 확인이 비밀번호와 일치하는지 체크
        '''
        if v != values['password1']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="입력된 비밀번호가 서로 다릅니다.")