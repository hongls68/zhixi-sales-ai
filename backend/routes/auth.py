"""
智析销售AI - 认证路由
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from database import get_db
from models.user import User
from services.auth_service import hash_password, create_access_token, decode_access_token

router = APIRouter(prefix="/api/auth", tags=["认证"])


# ============ 请求模型 ============

class SendCodeRequest(BaseModel):
    phone: str


class LoginRequest(BaseModel):
    phone: str
    code: str


class RegisterRequest(BaseModel):
    phone: str
    code: str
    password: str
    nickname: Optional[str] = ""


# ============ 接口实现 ============

@router.post("/send-code")
async def send_code(body: SendCodeRequest, db: Session = Depends(get_db)):
    """发送验证码（Mock：任意6位数字都行）"""
    if len(body.phone) != 11 or not body.phone.startswith("1"):
        raise HTTPException(400, "手机号格式不正确")

    # Mock模式：直接返回成功
    # 实际应该发送短信验证码
    return {"message": "验证码已发送", "phone": body.phone}


@router.post("/login")
async def login(body: LoginRequest, db: Session = Depends(get_db)):
    """登录（Mock：验证码123456）"""
    if body.code != "123456":
        raise HTTPException(400, "验证码错误")

    # 查找或创建用户
    user = db.query(User).filter(User.phone == body.phone).first()
    if not user:
        user = User(
            phone=body.phone,
            nickname="用户" + body.phone[-4:],
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    if not user.is_active:
        raise HTTPException(403, "账号已被禁用")

    # 更新登录时间
    user.last_login = datetime.utcnow()
    db.commit()

    # 生成Token
    token = create_access_token({"sub": str(user.id), "phone": user.phone})

    return {
        "token": token,
        "user": user.to_dict()
    }


@router.post("/register")
async def register(body: RegisterRequest, db: Session = Depends(get_db)):
    """注册"""
    if body.code != "123456":
        raise HTTPException(400, "验证码错误")

    if len(body.password) < 6:
        raise HTTPException(400, "密码至少6位")

    # 检查手机号是否已注册
    existing = db.query(User).filter(User.phone == body.phone).first()
    if existing:
        raise HTTPException(400, "该手机号已注册")

    # 创建用户
    user = User(
        phone=body.phone,
        nickname=body.nickname or "用户" + body.phone[-4:],
        password_hash=hash_password(body.password),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # 生成Token
    token = create_access_token({"sub": str(user.id), "phone": user.phone})

    return {
        "token": token,
        "user": user.to_dict()
    }
