"""
智析销售AI - 认证路由
支持手机号/用户名登录
"""
import re
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models.user import User
from services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["认证"])


# ============ 请求模型 ============

class SendCodeRequest(BaseModel):
    phone: str


class LoginRequest(BaseModel):
    account: str  # 手机号或用户名
    password: str


class RegisterRequest(BaseModel):
    phone: str
    code: str
    password: str
    username: Optional[str] = None  # 用户名（选填）
    email: Optional[str] = None  # 邮箱（选填）
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
    """登录（手机号或用户名 + 密码）"""
    account = body.account.strip()

    # 查找用户：支持手机号或用户名
    user = db.query(User).filter(
        or_(
            User.phone == account,
            User.username == account
        )
    ).first()

    if not user:
        raise HTTPException(400, "用户不存在")

    # 验证密码
    if not user.password_hash or not verify_password(body.password, user.password_hash):
        raise HTTPException(400, "密码错误")

    # 检查账号状态
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
    """注册（手机号+验证码+密码，用户名和邮箱选填）"""
    # 验证验证码（Mock：123456）
    if body.code != "123456":
        raise HTTPException(400, "验证码错误")

    # 验证密码长度
    if len(body.password) < 6:
        raise HTTPException(400, "密码至少6位")

    # 检查手机号是否已注册
    existing = db.query(User).filter(User.phone == body.phone).first()
    if existing:
        raise HTTPException(400, "该手机号已注册")

    # 检查用户名格式（如果填写了）
    if body.username:
        username = body.username.strip()
        # 用户名：字母+数字，4-20位
        if not re.match(r'^[a-zA-Z0-9]{4,20}$', username):
            raise HTTPException(400, "用户名格式不正确（4-20位字母+数字）")

        # 检查用户名是否已存在
        existing_username = db.query(User).filter(User.username == username).first()
        if existing_username:
            raise HTTPException(400, "该用户名已被使用")

    # 检查邮箱格式（如果填写了）
    if body.email:
        email = body.email.strip()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise HTTPException(400, "邮箱格式不正确")

        # 检查邮箱是否已存在
        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            raise HTTPException(400, "该邮箱已被注册")

    # 创建用户
    user = User(
        phone=body.phone,
        username=body.username.strip() if body.username else None,
        email=body.email.strip() if body.email else None,
        nickname=body.nickname or "用户" + body.phone[-4:],
        password_hash=hash_password(body.password),
        role="user",
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
