from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 本ファイルはDBの設定を定義するファイルである

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# CRUD操作に必要
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session:DBへの「接続〜切断」までの一連の流れ
# bind = engineで一つ上で作成したengine = create....に接続する（bind:接続）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# データベースのモデルクラスの継承
Base = declarative_base()