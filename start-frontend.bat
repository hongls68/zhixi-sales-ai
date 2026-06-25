@echo off
chcp 65001 >nul
echo ========================================
echo   智析销售AI - 前端启动
echo ========================================
echo.

cd /d "%~dp0frontend"

echo [1/2] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.9+
    pause
    exit /b 1
)

echo [2/2] 启动前端服务...
echo.
echo 访问地址：http://localhost:5500
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

python -m http.server 5500

pause
