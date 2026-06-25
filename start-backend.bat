@echo off
chcp 65001 >nul
echo ========================================
echo   智析销售AI - 后端启动
echo ========================================
echo.

cd /d "%~dp0backend"

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.9+
    pause
    exit /b 1
)

echo [2/3] 检查依赖...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo 首次运行，安装依赖...
    pip install -r requirements.txt
)

echo [3/3] 启动后端服务...
echo.
echo 访问地址：http://localhost:8000
echo API文档：http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

python main.py

pause
