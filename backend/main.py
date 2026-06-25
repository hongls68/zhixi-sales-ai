"""
智析销售AI - FastAPI 后端入口
本地优先，API兜底
"""
import sys
import io
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from config import BACKEND_PORT, DEBUG, FRONTEND_URL
from routes import auth_router, analysis_router, user_router, admin_router

# ============ App 初始化 ============
app = FastAPI(
    title="智析销售AI",
    version="2.0.0",
    description="智能销售分析平台API"
)

# CORS配置
ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ 启动事件 ============
@app.on_event("startup")
async def startup():
    """初始化数据库"""
    init_db()
    print("=" * 50)
    print("  智析销售AI 后端服务启动成功")
    print("=" * 50)
    print(f"  API文档: http://localhost:{BACKEND_PORT}/docs")
    print(f"  前端地址: {FRONTEND_URL}")
    print("=" * 50)


# ============ 挂载路由 ============
app.include_router(auth_router)
app.include_router(analysis_router)
app.include_router(user_router)
app.include_router(admin_router)


# ============ 健康检查 ============
@app.get("/")
async def root():
    return {
        "name": "智析销售AI",
        "version": "2.0.0",
        "status": "running",
        "docs": f"http://localhost:{BACKEND_PORT}/docs"
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


# ============ 启动入口 ============
if __name__ == "__main__":
    import uvicorn

    # 设置输出编码
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    print("智析销售AI 后端服务启动中...")
    print(f"访问 http://localhost:{BACKEND_PORT}")
    print(f"API文档 http://localhost:{BACKEND_PORT}/docs")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=BACKEND_PORT,
        reload=DEBUG
    )
