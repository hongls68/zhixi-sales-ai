"""
智析销售AI - 配置文件
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ============ 服务配置 ============
BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# ============ 数据库配置 ============
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./zhixi_sales.db")

# ============ JWT配置 ============
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "zhixi-sales-ai-secret-key-2026")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 1440))  # 24小时

# ============ AI配置 ============
# AI提供商：api（兼容OpenAI）或 ollama（本地）
AI_PROVIDER = os.getenv("AI_PROVIDER", "api")

# 兼容OpenAI的API配置
API_BASE_URL = os.getenv("API_BASE_URL", "https://token-plan-cn.xiaomimimo.com/v1")
API_KEY = os.getenv("API_KEY", "tp-c8wqvgrfoaa6e721ii615h8tgat0b859p28gslczbijin7ea")
API_MODEL = os.getenv("API_MODEL", "mimo-v2.5-pro")

# Ollama配置（本地开发，备用）
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5")

# ============ CORS配置 ============
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5500")
