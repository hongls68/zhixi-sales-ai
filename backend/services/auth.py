"""
智析 AI - 认证服务（JWT、密码哈希）

新密码使用 bcrypt 哈希；旧的 SHA-256 哈希在登录验证成功后自动迁移到 bcrypt。
"""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
import bcrypt as _bcrypt

from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES


def hash_password(password: str) -> str:
    """使用 bcrypt 哈希密码"""
    return _bcrypt.hashpw(password.encode("utf-8"), _bcrypt.gensalt()).decode("utf-8")


def is_sha256_hash(hashed_password: str) -> bool:
    """判断是否为旧的 SHA-256 哈希格式（salt$hash）"""
    return "$" in hashed_password and len(hashed_password.split("$")) == 2 and not hashed_password.startswith("$2")


def _verify_sha256(password: str, hashed_password: str) -> bool:
    """验证旧的 SHA-256 哈希"""
    try:
        salt, hashed = hashed_password.split("$")
        check_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return check_hash == hashed
    except Exception:
        return False


def verify_password(password: str, hashed_password: str) -> bool:
    """验证密码，兼容 bcrypt 和旧的 SHA-256 格式"""
    if is_sha256_hash(hashed_password):
        return _verify_sha256(password, hashed_password)
    return _bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def needs_rehash(hashed_password: str) -> bool:
    """判断密码是否需要重新哈希（旧格式 -> bcrypt）"""
    return is_sha256_hash(hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT 访问令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间（可选）
    
    Returns:
        JWT 令牌字符串
    """
    to_encode = data.copy()
    
    # 设置过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # 编码 JWT
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    解码 JWT 访问令牌
    
    Args:
        token: JWT 令牌字符串
    
    Returns:
        解码后的数据，如果令牌无效或过期则返回 None
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


def generate_reset_token(email: str) -> str:
    """
    生成密码重置令牌
    
    Args:
        email: 用户邮箱
    
    Returns:
        重置令牌
    """
    # 使用时间戳 + 随机数 + 邮箱生成令牌
    timestamp = datetime.utcnow().timestamp()
    random_part = secrets.token_hex(16)
    token_data = f"{email}:{timestamp}:{random_part}"
    
    # 使用 SHA-256 生成令牌
    token = hashlib.sha256(token_data.encode()).hexdigest()
    
    return token


def generate_verification_token(email: str) -> str:
    """
    生成邮箱验证令牌
    
    Args:
        email: 用户邮箱
    
    Returns:
        验证令牌
    """
    return generate_reset_token(email)
