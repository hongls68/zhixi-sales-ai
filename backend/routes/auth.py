"""
智析 AI - 认证路由
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from deps import get_current_user
from schemas.user import (
    RegisterRequest,
    LoginRequest,
    MeResponse,
    SendCodeRequest,
    SendCodeResponse,
    VerifyRequest,
    VerifyResponse,
)
from services import (
    hash_password,
    verify_password,
    needs_rehash,
    create_access_token,
    generate_verification_code,
    send_verification_email,
)

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register")
async def register(body: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册"""
    if len(body.username) < 3 or len(body.username) > 20:
        raise HTTPException(400, "用户名长度 3-20 字符")
    if len(body.password) < 6:
        raise HTTPException(400, "密码至少 6 位")
    if db.query(models.User).filter(models.User.username == body.username).first():
        raise HTTPException(400, "用户名已存在")
    if db.query(models.User).filter(models.User.email == body.email).first():
        raise HTTPException(400, "邮箱已注册")

    user = models.User(
        username=body.username,
        email=body.email,
        password_hash=hash_password(body.password),
        is_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    db.add(models.AccessLog(user_id=user.id, action="register"))
    db.commit()

    token = create_access_token({"sub": str(user.id), "username": user.username, "role": user.role})
    return {
        "token": token,
        "user": {"id": user.id, "username": user.username, "email": user.email, "role": user.role},
    }


@router.post("/login")
async def login(body: LoginRequest, db: Session = Depends(get_db)):
    """用户登录（支持用户名或邮箱）"""
    user = db.query(models.User).filter(
        (models.User.username == body.username) | (models.User.email == body.username)
    ).first()

    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "用户名或密码错误")
    if not user.is_active:
        raise HTTPException(403, "账号已被禁用")

    # 旧 SHA-256 密码自动迁移到 bcrypt
    if needs_rehash(user.password_hash):
        user.password_hash = hash_password(body.password)

    user.last_login = datetime.utcnow()
    db.add(models.AccessLog(user_id=user.id, action="login"))
    db.commit()

    token = create_access_token({"sub": str(user.id), "username": user.username, "role": user.role})
    return {
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "avatar": user.avatar,
        },
    }


@router.get("/me")
async def get_me(user: models.User = Depends(get_current_user)):
    """获取当前用户信息"""
    if not user:
        raise HTTPException(401, "未登录")
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "avatar": user.avatar,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


@router.post("/send-code", response_model=SendCodeResponse)
async def send_code(body: SendCodeRequest, db: Session = Depends(get_db)):
    """发送邮箱验证码"""
    code = generate_verification_code()
    sent = send_verification_email(body.email, code)
    if not sent:
        raise HTTPException(500, "验证码发送失败，请稍后重试")
    # 验证码存入数据库
    from datetime import timedelta
    from config import VERIFICATION_CODE_EXPIRE_MINUTES
    verification = models.EmailVerification(
        email=body.email,
        code=code,
        expired_at=datetime.utcnow() + timedelta(minutes=VERIFICATION_CODE_EXPIRE_MINUTES),
    )
    db.add(verification)
    db.commit()
    return SendCodeResponse(message="验证码已发送", email=body.email)


@router.post("/verify", response_model=VerifyResponse)
async def verify_email(body: VerifyRequest, db: Session = Depends(get_db)):
    """验证邮箱验证码"""
    record = (
        db.query(models.EmailVerification)
        .filter(models.EmailVerification.email == body.email, models.EmailVerification.used == False)
        .order_by(models.EmailVerification.created_at.desc())
        .first()
    )
    if not record:
        raise HTTPException(400, "请先发送验证码")
    if record.is_expired():
        raise HTTPException(400, "验证码已过期，请重新发送")
    if record.code != body.code:
        raise HTTPException(400, "验证码错误")

    record.used = True
    # 标记用户已验证
    user = db.query(models.User).filter(models.User.email == body.email).first()
    if user:
        user.is_verified = True
    db.commit()
    return VerifyResponse(message="邮箱验证成功", email=body.email)
