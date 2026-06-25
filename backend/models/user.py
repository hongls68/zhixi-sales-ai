"""
智析销售AI - 用户模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
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
