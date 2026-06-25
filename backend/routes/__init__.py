"""
智析 AI - 路由包
"""
from routes.auth import router as auth_router
from routes.admin import router as admin_router
from routes.report import router as report_router

__all__ = ["auth_router", "admin_router", "report_router"]
