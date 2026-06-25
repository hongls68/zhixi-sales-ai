"""
智析 AI - 用户数据模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户 ID")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    email = Column(String(255), unique=True, nullable=False, index=True, comment="邮箱")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    role = Column(String(20), default="user", comment="角色：user/admin")
    avatar = Column(String(200), default="", comment="头像")
    is_verified = Column(Boolean, default=False, comment="是否已验证邮箱")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    last_login = Column(DateTime, comment="最后登录时间")

    reports = relationship("Report", back_populates="user")
    logs = relationship("AccessLog", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, role={self.role})>"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "avatar": self.avatar,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }


class Report(Base):
    """报告表"""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="报告 ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户 ID")
    content = Column(Text, nullable=False, comment="输入内容")
    report = Column(Text, nullable=False, comment="生成报告")
    style = Column(String(20), default="professional", comment="风格")
    report_type = Column(String(20), default="weekly", comment="报告类型：daily/weekly/monthly")
    ai_model = Column(String(50), default="deepseek", comment="AI 模型")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    user = relationship("User", back_populates="reports")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "report": self.report,
            "style": self.style,
            "report_type": self.report_type,
            "ai_model": self.ai_model,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class AccessLog(Base):
    """访问日志表"""
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="日志 ID")
    user_id = Column(Integer, ForeignKey("users.id"), comment="用户 ID")
    action = Column(String(50), comment="操作：login/register/generate/view")
    ip_address = Column(String(45), comment="IP 地址")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    user = relationship("User", back_populates="logs")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
