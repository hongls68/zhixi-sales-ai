"""
智析 AI - 邮箱验证数据模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base


class EmailVerification(Base):
    """邮箱验证表"""
    __tablename__ = "email_verifications"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="验证 ID")
    email = Column(String(255), nullable=False, index=True, comment="邮箱")
    code = Column(String(6), nullable=False, comment="6 位验证码")
    expired_at = Column(DateTime, nullable=False, comment="过期时间")
    used = Column(Boolean, default=False, comment="是否已使用")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    def __repr__(self):
        return f"<EmailVerification(id={self.id}, email={self.email}, code={self.code}, expired_at={self.expired_at})>"

    def is_expired(self):
        """检查是否已过期"""
        return datetime.utcnow() > self.expired_at

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "email": self.email,
            "code": self.code,
            "expired_at": self.expired_at.isoformat() if self.expired_at else None,
            "used": self.used,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }