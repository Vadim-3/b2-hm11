from sqlalchemy.orm import Session
from app.database.models import User
from app.schemas import UserSchema


async def get_users(skip: int, limit: int, db: Session) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


async def get_user(user_id: int, db: Session) -> User:
    return db.query(User).filter(User.id == user_id).first()


async def get_birthday(today, end_date, db: Session):
    users = db.query(User).all()
    result = []
    for user in users:
        if (
                user.birthday_date.month >= today.month and user.birthday_date.day >= today.day and user.birthday_date.month <= end_date.month and user.birthday_date.day <= end_date.day):
            result.append(user)
    return result


async def search_users(first_name: str | None, last_name: str | None, email: str | None, db: Session):
    result = []
    users = db.query(User).all()
    for user in users:
        if first_name != None:
            if user.first_name == first_name:
                result.append(user)
        if last_name != None:
            if user.last_name == last_name:
                result.append(user)
        if email != None:
            if user.email == email:
                result.append(user)
    return result


async def create_users(body: UserSchema, db: Session) -> User:
    user_ = User(first_name=body.first_name, last_name=body.last_name, birthday_date=body.birthday_date,
                 emails=body.emails, phone_numbers=body.phone_numbers, other_description=body.other_description)
    db.add(user_)
    db.commit()
    db.refresh(user_)
    return user_


async def update_user(user_id: int, body: UserSchema, db: Session) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.first_name = body.first_name
        user.last_name = body.last_name
        user.phone_numbers = body.phone_numbers
        user.emails = body.emails
        user.other_description = body.other_description
        db.commit()
    return user


async def remove_user(user_id: int, db: Session) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
