from passlib.context import CryptContext
from sqlalchemy.orm import Session
from accountapp.schema import UserCreateSchema
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(user_info: UserCreateSchema, db: Session):
    new_user = User(
        username=user_info.username,
        password=pwd_context.hash(user_info.password1),
        email=user_info.email,
    )
    db.add(new_user)
    db.commit()

def get_user(user_info: UserCreateSchema, db: Session):
    return db.query(User).filter(
        (User.username == user_info.username) |
        (User.email == user_info.email)
    ).first()