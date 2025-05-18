from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 从 .env 获取 DATABASE_URL，默认使用本地 SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")

# 根据数据库类型设置连接参数
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    connect_args = {"sslmode": "require"}

# 创建数据库引擎
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基类
Base = declarative_base()

# 获取数据库 Session 的依赖函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
