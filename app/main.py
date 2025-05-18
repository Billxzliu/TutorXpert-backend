# app/main.py

from fastapi import FastAPI
from app.database import Base, engine
from app.routes import student

app = FastAPI(
    title="GlowUpTutors API",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 添加这一段
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以改为你的前端 URL，例如 ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建数据库表结构（仅在第一次运行时）
Base.metadata.create_all(bind=engine)

# 加载路由
app.include_router(student.router)

@app.get("/")
def root():
    return {"message": "GlowUpTutors backend is running."}
