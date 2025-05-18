# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()

# 从环境变量读取 DATABASE_URL，如果没有就用本地 SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./student.db")

# SQLite 需要一个额外参数
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# 创建数据库引擎
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# 创建 SessionLocal 类，用于生成 session 实例
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 Base 类，用于定义模型表结构
Base = declarative_base()

# FastAPI 路由中依赖注入的数据库 session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
