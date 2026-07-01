"""
智析销售AI - 用户模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    nickname = Column(String(50), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")  # user, admin
    industry = Column(String(100), nullable=True)  # 行业
    job_title = Column(String(100), nullable=True)  # 职位
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    analyses = relationship("Analysis", back_populates="user")
    access_logs = relationship("AccessLog", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "nickname": self.nickname,
            "role": self.role,
            "industry": self.industry,
            "job_title": self.job_title,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class AccessLog(Base):
    """访问日志"""
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="access_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class OperationLog(Base):
    """操作日志"""
    __tablename__ = "operation_logs"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, index=True)
    admin_name = Column(String(50), nullable=True)
    action = Column(String(50), nullable=False)
    target_type = Column(String(50), nullable=True)  # user, analysis
    target_id = Column(Integer, nullable=True)
    detail = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

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
            "created_at": self.created_at.isoformat() if sel