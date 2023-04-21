from fastapi import APIRouter, HTTPException, status, Depends
from passlib.context import CryptContext

from modules.auth import genAccessToken, genRefreshToken

from database import conn
from accountapp import schema

router = APIRouter(
    prefix="/api/user",
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup", status_code=status.HTTP_204_NO_CONTENT)
def signup(user_info: schema.UserCreateSchema):

    user_id = user_info.user_id
    password_hash = pwd_context.hash(user_info.password)
    nickname = user_info.nickname
    email = user_info.email

    with conn.cursor() as db:
        db.execute(f'SELECT * FROM ACCOUNT WHERE id={user_id}')
        rows = db.fetchall()
    
    if len(rows):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="user already exists")
    
    with conn.cursor() as db:
        db.execute(f'INSERT INTO ACCOUNT (user_id, password_hash, nickname, email) VALUES ({user_id}, {password_hash}, {nickname}, {email})')
        db.commit()

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_info: schema.UserLoginSchema):

    user_id = user_info.user_id
    password_hash = pwd_context.hash(user_info.password)

    with conn.cursor() as db:
        db.execute(f'SELECT (user_id, password_hash, nickname, email) FROM ACCOUNT WHERE id={user_id} AND password_hash={password_hash}')
        rows = db.fetchall()
    
    if not len(rows):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="invalid ID or PW")
    
    row = rows[0]
    nickname = row[2]
    email = row[3]

    access_token = genAccessToken({
        'user_id': user_id,
        'password_hash': password_hash,
        'nickname': nickname,
        'email': email,
    })
    refresh_token = genRefreshToken()

    with conn.cursor() as db:
        db.execute(f'UPDATE ACCOUNT SET refresh_token={refresh_token} WHERE user_id={user_id}')
        db.commit()

    # cookie로 리프레시 토큰 전송
    
    return {
        'access_token': access_token,
        'detail': 'login success'
    }

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(user_info: schema.UserLogoutSchema):

    refresh_token = user_info.refresh_token

    with conn.cursor() as db:
        db.execute(f'UPDATE ACCOUNT SET refresh_token=NULL WHERE refresh_token={refresh_token}')
        db.commit()

    return {
        'detail': 'logout success'
    }

@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh():
    # cookie에서 refresh token 가져옴
    refresh_token = ''

    with conn.cursor() as db:
        db.execute(f'SELECT (user_id, password_hash, nickname, email) FROM ACCOUNT WHERE refresh_token={refresh_token}')
        rows = db.fetchall()

    if not len(rows):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="invalid refresh token")
    
    row = rows[0]
    user_id = row[0]
    password_hash = row[1]
    nickname = row[2]
    email = row[3]

    access_token = genAccessToken({
        'user_id': user_id,
        'password_hash': password_hash,
        'nickname': nickname,
        'email': email,
    })
    refresh_token = genRefreshToken()

    with conn.cursor() as db:
        db.execute(f'UPDATE ACCOUNT SET refresh_token={refresh_token} WHERE user_id={user_id}')
        db.commit()
    
    return {
        'access_token': access_token,
        'detail': 'login success'
    }

@router.put("/update")
def update():
    # 비밀번호와 이메일 바꾸는 기능
    pass