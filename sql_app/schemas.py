import datetime
from pydantic import BaseModel
from typing import Union

# FastAPI側のデータ構造を定義する
# postメソッド実行時、idは一意に作成されるためCREATEの型には入れてはいけない
# DBの構造としてはbooking_id,user_id,institution_idは必要だが、JsonデータでIDは送らない
# models.pyのprimary_keyと設定されているカラム情報は不要

class CreateBooking(BaseModel):
    user_id:int
    institution_id:int
    riservation_number:int
    date:datetime.date
    start:datetime.time
    end:datetime.time

# 継承するため変数不要
class Booking(CreateBooking):
    booking_id:int

    class Config:
        orm_mode = True
    

class CreateUser(BaseModel):
    user_name:str
    
class User(CreateUser):
    user_id:int

    class Config:
        orm_mode = True



class CreateInstitution(BaseModel):
    institution_name:str
    institution_capacity:int
    institution_rank:int
    institution_starttime:datetime.time
    institution_endtime:datetime.time
    
class Institution(CreateInstitution):
    institution_id:int
    
    class Config:
        orm_mode = True