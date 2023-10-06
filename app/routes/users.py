from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.database.connect import get_db
from app.schemas import UserSchema, UserResponse
from app.repository import users as repository_users

router = APIRouter(prefix='/users', tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = await repository_users.get_users(skip, limit, db)
    return users


@router.get("/birthdays", response_model=list[UserResponse])
async def read_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    end_date = today + timedelta(days=7)
    birthdays = await repository_users.get_birthday(today, end_date, db)
    if birthdays is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return birthdays


@router.get("/search", response_model=list[UserResponse])
async def search(db: Session = Depends(get_db), first_name: str = Query(None), last_name: str = Query(None),
                 email: str = Query(None)):
    users = await repository_users.search_users(first_name, last_name, email, db)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    users = await repository_users.get_user(user_id, db)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return users


@router.post("/", response_model=UserResponse)
async def create_users(body: UserSchema, db: Session = Depends(get_db)):
    return await repository_users.create_users(body, db)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(body: UserSchema, user_id: int, db: Session = Depends(get_db)):
    user = await repository_users.update_user(user_id, body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=UserResponse)
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = await repository_users.remove_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
