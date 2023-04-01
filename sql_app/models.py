from sqlalchemy import Column, ForeignKey, Integer, String,DateTime,Time

from .database import Base

# データベースの構造定義ファイル

class User(Base):
    __tablename__ = "users"
    # user_idはprimary（主キーのため自動的に一意に設定される）
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String,index=True)


class Institution(Base):
    __tablename__ = "institutions"

    institution_id = Column(Integer, primary_key=True, index=True)
    institution_name = Column(String,unique=True, index=True)
    institution_capacity = Column(Integer)
    institution_starttime = Column(Time,nullable=False)
    institution_endtime  = Column(Time,nullable=False)


class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, index=True)
    # Foreinkey 親データ(usersテーブルのuser_id)が削除されたらこのデータも削除される
    user_id = Column(Integer, ForeignKey('users.user_id',ondelete='SET NULL'),nullable=False)
    institution_id = Column(Integer, ForeignKey('institutions.institution_id',ondelete='SET NULL'),nullable=False)
    riservation_number = Column(Integer,nullable=False)
    date = Column(DateTime,nullable=False)
    start = Column(Time,nullable=False)
    end = Column(Time,nullable=False)

