"""
智析 AI - 数据库连接配置
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# 创建数据库引擎
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # SQLite 需要
    )
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"charset": "utf8mb4"},  # MySQL 连接参数
        pool_pre_ping=True,  # 自动检测无效连接
        pool_recycle=3600,   # 连接回收时间
    )

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()


def get_db():
    """
    获取数据库会话的依赖函数
    使用 yield 确保会话在使用后正确关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库表
    """
    from models.user import User, Report, AccessLog
    Base.metadata.create_all(bind=engine)