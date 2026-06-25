"""
智析销售AI - 路由模块
"""
from routes.auth import router as auth_router
from routes.analysis import router as analysis_router
from routes.user import router as user_router

__all__ = ["auth_router", "analysis_router", "user_router"]
