"""
智析销售AI - 用户模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)  # 手机号（必填）
    username = Column(String(50), unique=True, index=True, nullable=True)  # 用户名（选填）
    email = Column(String(100), unique=True, index=True, nullable=True)  # 邮箱（选填）
    nickname = Column(String(50), default="")
    password_hash = Column(String(255), default="")
    avatar = Column(String(200), default="")
    company = Column(String(100), default="")
    job_title = Column(String(100), default="")
    industry = Column(String(50), default="")
    role = Column(String(20), default="user")  # user / admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "username": self.username,
            "email": self.email,
            "nickname": self.nickname,
            "avatar": self.avatar,
            "company": self.company,
            "job_title": self.job_title,
            "industry": self.industry,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }


class AccessLog(Base):
    """访问日志表"""
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)  # login / view / generate
    ip_address = Column(String(50), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="logs")


class OperationLog(Base):
    """管理员操作日志表"""
    __tablename__ = "operation_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    admin_name = Column(String(50), default="")
    action = Column(String(50), nullable=False)  # delete_user / update_user / disable_user / enable_user / delete_analysis
    target_type = Column(String(20), default="")  # user / analysis
    target_id = Column(Integer, nullable=True)
    detail = Column(String(500), default="")
    ip_address = Column(String(50), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    admin = relationship("User", foreign_keys=[admin_id], backref="operations")

    def to_dict(self):
        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "admin_name": self.admin_name,
            "action": self.action,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "detail": self.detail,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
