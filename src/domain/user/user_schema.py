from fastapi import status, HTTPException
from pydantic import BaseModel, validator, EmailStr

class CreateUser(BaseModel):
    email: EmailStr
    fullname: str
    password1: str
    password2: str

    @validator('email','fullname','password1','password2')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="빈 칸을 모두 채워주세요")
        return v
    
    @validator('password2')
    def password_check(cls, v, values):
        if v != values['password1']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="입력된 비밀번호가 서로 다릅니다.")