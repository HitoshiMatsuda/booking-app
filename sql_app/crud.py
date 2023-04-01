from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

# CRUD操作を定義する

# @matsuda
# ユーザー一覧を取得
# skip,limitはデータ取得方法を指定するオプション
# READの取得条件
# db.query(models.User)はデータベースの読み込み先を指定。models.pyのUserテーブル
def get_users(db: Session, skip: int=0, limit:int=100):
    return db.query(models.User).offset(skip).limit(limit).all()
    # return db.query(models.User).filter(models.User.id == user_id).first()


# @matsuda
# 施設一覧を取得
def get_institutions(db: Session, skip: int=0, limit:int=100):
    return db.query(models.Institution).offset(skip).limit(limit).all()
    # return db.query(models.User).filter(models.User.email == email).first()


# @matsuda
# 予約一覧を取得
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()


# @matsuda
# ユーザー情報を登録
# CREATEの流れ
# ①フォーム上でユーザー名を入力
# ②送信ボタン押下時にAPI実行
# ③FastAPIでデータを受け取る（schemas.pyのUserクラスのデータ構造で取得）
# ④受け取ったデータをDBへ書き込む
def create_user(db: Session, user: schemas.User):
    # インスタンスの生成
    # user_idは一意に設定されるため受け取り不要
    db_user = models.User(user_name=user.user_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
    # fake_hashed_password = user.password + "notreallyhashed"
    # db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    # db.add(db_user)
    # db.commit()
    # db.refresh(db_user)
    # return db_user

# @matsuda
# 施設情報を登録
def create_institution(db: Session, institution: schemas.Institution):
    db_institution = models.Institution(
        institution_name=institution.institution_name,
        institution_capacity=institution.institution_capacity,
        institution_starttime=institution.institution_starttime,
        institution_endtime=institution.institution_endtime
        )
    db.add(db_institution)
    db.commit()
    db.refresh(db_institution)
    return db_institution

# @matsuda
# 予約情報を登録
def create_booking(db: Session, booking: schemas.Booking):
    # 予約の重複チェックロジック
    # 施設、日付、時間帯が重複するか
    db_booked = db.query(models.Booking).filter(models.Booking.institution_id == booking.institution_id).filter(models.Booking.date == booking.date).filter(models.Booking.end > booking.start).filter(models.Booking.start < booking.end).all()


    # 重複なし
    if len(db_booked) == 0:                
        db_booking = models.Booking(
            user_id = booking.user_id,
            institution_id = booking.institution_id,
            riservation_number = booking.riservation_number,
            date = booking.date,
            start = booking.start,
            end = booking.end
            )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking
    # 重複あり
    else:
        raise HTTPException(status_code=404, detail="Already booked")