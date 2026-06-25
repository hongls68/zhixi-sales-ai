"""
智析 AI - 统一认证依赖
"""
from typing import Optional
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import User
from services import decode_access_token


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> Optional[User]:
    """从 Authorization header 解析 JWT，返回用户或 None"""
    auth_header: str = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header[7:]
    payload = decode_access_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user and user.is_active:
        return user
    return None


async def require_user(
    user: Optional[User] = Depends(get_current_user),
) -> User:
    """要求已登录，否则 401"""
    if not user:
        raise HTTPException(status_code=401, detail="未登录或令牌已过期")
    return user


async def require_admin(
    user: User = Depends(require_user),
) -> User:
    """要求管理员权限，否则 403"""
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return user
