from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from database import get_db
from accountapp import crud, schema

router = APIRouter(
    prefix="/api/user",
)

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def signup(user_info: schema.UserCreateSchema, db: Session = Depends(get_db)):
    exist_user_info = crud.get_user(user_info=user_info, db=db)
    if exist_user_info:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    crud.create_user(user_info=user_info, db=db)