"""
智析 AI - WeeklyReport Pro v3.0
主应用入口：初始化、中间件、页面路由、路由挂载
"""

import os
import sys
import io
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from database import init_db, SessionLocal
from models import User
from services import hash_password
from config import FRONTEND_URL
from routes import auth_router, admin_router, report_router

# ============ App 初始化 ============
app = FastAPI(title="智析 AI - WeeklyReport Pro", version="3.0.0")

# CORS - 仅允许本地开发 + 配置的前端地址
ALLOWED_ORIGINS = list(dict.fromkeys(
    o for o in [
        "http://localhost:8080",
        "http://localhost:5500",
        "http://localhost:5173",
        FRONTEND_URL,
    ] if o
))

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ 路径配置 ============
BASE_DIR = Path(__file__).resolve().parent.parent  # Smart Analysis/
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = TEMPLATES_DIR / "static"

# 挂载静态文件
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _read_html(filename: str) -> str:
    """读取前端 HTML 文件"""
    path = TEMPLATES_DIR / filename
    if not path.exists():
        return f"<html><body><h1>页面未找到：{filename}</h1></body></html>"
    return path.read_text(encoding="utf-8")


# 预加载页面模板
INDEX_HTML = _read_html("index.html")
LOGIN_HTML = _read_html("login.html")
REGISTER_HTML = _read_html("register.html")
HOME_HTML = _read_html("home.html")


# ============ 启动事件 ============
@app.on_event("startup")
def startup():
    init_db()
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@zixiai.com",
                password_hash=hash_password("admin123"),
                role="admin",
                is_verified=True,
            )
            db.add(admin)
            db.commit()
            print("[OK] 默认管理员创建成功：admin / admin123")
    finally:
        db.close()


# ============ 挂载路由 ============
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(report_router)


# ============ 页面路由 ============
@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content=INDEX_HTML)


@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return HTMLResponse(content=LOGIN_HTML)


@app.get("/register", response_class=HTMLResponse)
async def register_page():
    return HTMLResponse(content=REGISTER_HTML)


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    from deps import get_current_user
    from database import get_db
    db = next(get_db())
    try:
        user = await get_current_user(request, db)
    finally:
        db.close()
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return HTMLResponse(content=HOME_HTML)


# ============ 启动入口 ============
if __name__ == "__main__":
    import uvicorn
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    print("智析 AI - WeeklyReport Pro v3.0 启动中...")
    print("访问 http://localhost:8080")
    print("默认管理员：admin / admin123")
    uvicorn.run(app, host="0.0.0.0", port=8080)
