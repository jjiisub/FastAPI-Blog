from pydantic import BaseModel, validator, EmailStr

class CreateUser(BaseModel):
    email: EmailStr
    fullname: str
    password1: str
    password2: str

    @validator('email','fullname','password1','password2')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 칸을 모두 채워주세요")
        return v
    
    @validator('password2')
    def password_chk(cls, v, values):
        if v != values['password1']:
            raise ValueError('입력한 비밀번호가 비밀번호가 서로 다릅니다')


class Token(BaseModel):
    access_token: str
    token_type: str
    email: str