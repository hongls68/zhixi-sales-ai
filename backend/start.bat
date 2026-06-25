@echo off
chcp 65001 >nul

echo ========================================
echo   智析 AI - 后端服务启动脚本
echo ========================================

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM 检查 Python 版本
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 创建虚拟环境（如果不存在）
if not exist "venv" (
    echo 正在创建虚拟环境...
    python -m venv venv
)

REM 检查并使用正确的虚拟环境路径
if exist "..\venv" (
    echo 正在激活虚拟环境（根目录）...
    call ..\venv\Scripts\activate.bat
) else if exist "venv" (
    echo 正在激活虚拟环境...
    call venv\Scripts\activate.bat
) else (
    echo 正在创建虚拟环境...
    python -m venv venv
    call venv\Scripts\activate.bat
)

REM 安装依赖
echo 正在安装依赖...
pip install -r requirements.txt

REM 启动服务
echo.
echo ========================================
echo   启动后端服务...
echo   访问地址：http://localhost:8000
echo   API 文档：http://localhost:8000/docs
echo ========================================
echo.

python main.py

pause