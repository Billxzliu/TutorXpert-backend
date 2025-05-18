from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes import student

# ⛳ 重要：导入模型，确保 User 表被注册到 SQLAlchemy 的 Base 中
from app import models  # 必须添加这行，否则表不会被创建！

app = FastAPI(
    title="GlowUpTutors API",
    version="1.0.0"
)

# ✅ 添加跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 建议上线时替换为你的前端 URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 初始化数据库（必须在导入模型之后）
Base.metadata.create_all(bind=engine)

# ✅ 注册路由
app.include_router(student.router)

@app.get("/")
def root():
    return {"message": "GlowUpTutors backend is running."}
