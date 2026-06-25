#!/bin/bash

# 智析 AI 后端启动脚本

echo "================================"
echo "  智析 AI - 后端服务启动脚本"
echo "================================"

# 检查 Python 版本
python --version 2>&1
if [ $? -ne 0 ]; then
    echo "错误：未找到 Python，请先安装 Python 3.8+"
    exit 1
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "正在创建虚拟环境..."
    python -m venv venv
fi

# 激活虚拟环境
echo "正在激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "正在安装依赖..."
pip install -r requirements.txt

# 启动服务
echo ""
echo "================================"
echo "  启动后端服务..."
echo "  访问地址：http://localhost:8000"
echo "  API 文档：http://localhost:8000/docs"
echo "================================"
echo ""

python main.py