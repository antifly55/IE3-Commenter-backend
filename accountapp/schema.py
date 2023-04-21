from pydantic import BaseModel, validator, EmailStr


class UserCreateSchema(BaseModel):
    user_id: str
    password: str
    password_val: str
    nickname: str
    email: EmailStr

    @validator('user_id', 'password', 'password_val', 'nickname', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @validator('password_val')
    def passwords_match(cls, v, values):
        if v != values['password']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v
    
class UserLoginSchema(BaseModel):
    user_id: str
    password: str

class UserLogoutSchema(BaseModel):
    refresh_token: str