@echo off
echo ========================================
echo   听脑AI 登录系统启动脚本
echo ========================================
echo.

cd /d "%~dp0backend"

echo [1/2] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo 错误：未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/2] 启动后端服务...
echo 访问地址：http://localhost:8080
echo 登录页面：http://localhost:8080/login_new.html
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

python main.py

pause
