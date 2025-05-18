# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")  # 从 Render 环境中读取变量
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})  # 必须添加 sslmode=require

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# FastAPI 路由中依赖注入的数据库 session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
