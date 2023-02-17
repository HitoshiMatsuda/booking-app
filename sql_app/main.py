from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import crud,models,schemas
from .database import SessionLocal, engine

# データベースの作成
models.Base.metadata.create_all(bind = engine)
    
app = FastAPI()

# DBのセッションを確立
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get = READ / post = CREATE

# READ
@app.get('/users', response_model=List[schemas.User])
async def read_users(skip: int =0,limit: int =100,db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip,limit=limit)
    return users

@app.get('/institutions', response_model=List[schemas.Institution])
async def institutions(skip: int =0,limit: int =100,db: Session = Depends(get_db)):
    institutions = crud.get_institutions(db, skip=skip,limit=limit)
    return institutions

@app.get('/bookings', response_model=List[schemas.Booking])
async def bookings(skip: int =0,limit: int =100,db: Session = Depends(get_db)):
    bookings = crud.get_bookings(db, skip=skip,limit=limit)
    return bookings

# CREATE
@app.post('/users', response_model=schemas.User)
async def create_user(user: schemas.CreateUser,db: Session = Depends(get_db)):
    return crud.create_user(db=db,user=user)

@app.post('/institutions', response_model=schemas.Institution)
async def create_institution(institution: schemas.CreateInstitution,db: Session = Depends(get_db)):
    return crud.create_institution(db=db,institution=institution)

@app.post('/bookings', response_model=schemas.Booking)
async def create_booking(booking: schemas.CreateBooking,db: Session = Depends(get_db)):
    return crud.create_booking(db=db,booking=booking)