"""
智析销售AI - 数据库配置
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# 创建数据库引擎
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库表和默认数据"""
    from models.user import User, OperationLog
    from models.analysis import Analysis

    # 创建表
    Base.metadata.create_all(bind=engine)
    print("[OK] 数据库表创建完成")

    # 创建默认管理员
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.phone == "admin").first()
        if not admin:
            from services.auth_service import hash_password
            admin = User(
                phone="admin",
                nickname="管理员",
                password_hash=hash_password("admin123"),
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("[OK] 默认管理员创建成功：admin / admin123")
        else:
            print("[OK] 管理员账号已存在")
    except Exception as e:
        print(f"[WARN] 创建管理员失败: {e}")
        db.rollback()
    finally:
        db.close()
