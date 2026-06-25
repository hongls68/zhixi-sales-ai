"""
智析 AI - 配置文件
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置（默认使用 SQLite 本地数据库）
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./zixiai.db")

# JWT 配置
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "weekly-report-pro-secret-key-2026")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7))  # 7 天

# 旧版 JWT 配置（兼容）
SECRET_KEY = JWT_SECRET_KEY
ALGORITHM = JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = JWT_ACCESS_TOKEN_EXPIRE_MINUTES

# 邮件服务配置（QQ 邮箱示例）
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.qq.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "your-email@qq.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your-smtp-password")  # 授权码，非登录密码
SMTP_FROM = os.getenv("SMTP_FROM", "智析 AI <your-email@qq.com>")

# 前端地址（用于验证链接）
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# 验证码配置
VERIFICATION_CODE_EXPIRE_MINUTES = 5  # 验证码有效期 5 分钟
VERIFICATION_CODE_LENGTH = 6  # 验证码长度

# 频率限制配置
RATE_LIMIT_SECONDS = 60  # 1 分钟
MAX_VERIFICATION_ATTEMPTS = 3  # 最多尝试 3 次
