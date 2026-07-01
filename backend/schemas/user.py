"""
智析 AI - 用户请求/响应模型（Pydantic）
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# ==================== 注册相关 ====================

class RegisterRequest(BaseModel):
    """注册请求"""
    username: str
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    """注册响应"""
    token: str
    user: dict


# ==================== 登录相关 ====================

class LoginRequest(BaseModel):
    """登录请求 - 支持用户名或邮箱登录"""
    username: str  # 可以是用户名或邮箱
    password: str


class LoginResponse(BaseModel):
    """登录响应"""
    token: str
    user: dict


# ==================== 邮箱验证相关 ====================

class SendCodeRequest(BaseModel):
    """发送验证码请求"""
    email: EmailStr


class SendCodeResponse(BaseModel):
    """发送验证码响应"""
    message: str
    email: str


class VerifyRequest(BaseModel):
    """邮箱验证请求"""
    email: EmailStr
    code: str


class VerifyResponse(BaseModel):
    """邮箱验证响应"""
    message: str
    email: str


# ==================== 用户信息 ====================

class UserInfo(BaseModel):
    """用户信息"""
    id: int
    username: str
    email: str
    role: str
    avatar: str
    is_verified: bool
    is_active: bool
    created_at: Optional[str] = None
    last_login: Optional[str] = None

    class Config:
        from_attributes = True


class MeResponse(BaseModel):
    """获取当前用户响应"""
    id: int
    username: str
    email: str
    role: str
    avatar: str
    created_at: Optional[str] = None


# ==================== 报告相关 ====================

class GenerateRequest(BaseModel):
    """生成报告请求"""
    content: str
    style: str = "professional"
    report_type: str = "weekly"
    language: str = "zh"
    ai_model: str = "deepseek"
    custom_prompt: Optional[str] = None


class GenerateResponse(BaseModel):
    """生成报告响应"""
    report: str
    model: str
    style: str


class HistoryItem(BaseModel):
    """历史记录项"""
    id: int
    content: str
    report: str
    style: str
    type: str
    model: str
    created_at: str


class HistoryResponse(BaseModel):
    """历史记录响应"""
    history: list[HistoryItem]


# ==================== 管理员相关 ====================

class AdminStats(BaseModel):
    """管理员统计数据"""
    dau: int
    wau: int
    total_users: int
    today_users: int
    total_reports: int
    today_reports: int
    daily_regs: list[dict]
    daily_active: list[dict]
    model_usage: list[dict]


class UserListItem(BaseModel):
    """用户列表项"""
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: Optional[str] = None
    last_login: Optional[str] = None


class UserListResponse(BaseModel):
    """用户列表响应"""
    total: int
    page: int
    pages: int
    users: list[UserListItem]


class UpdateUserRequest(BaseModel):
    """更新用户请求"""
    role: Optional[str] = None
    is_active: Optional[bool] = None


class ReportItem(BaseModel):
    """报告项"""
    id: int
    user_id: int
    username: str
    content: str
    style: str
    type: str
    model: str
    created_at: str


class ReportListResponse(BaseModel):
    """报告列表响应"""
    total: int
    page: int
    pages: int
    reports: list[ReportItem]