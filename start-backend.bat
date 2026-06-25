@echo off
chcp 936 >nul
echo ========================================
echo   智析销售AI - 后端启动
echo ========================================
echo.

:: 强制切换到bat同目录下的backend文件夹
set "backend_dir=%~dp0backend"
if not exist "%backend_dir%" (
    echo 错误：未找到backend文件夹，请检查项目完整解压！
    pause
    exit /b 1
)
cd /d "%backend_dir%"

echo [1/3] 检测Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未检测到Python3.9及以上，请安装并配置环境变量
    pause
    exit /b 1
)

echo [2/3] 检查项目依赖
if not exist "requirements.txt" (
    echo 错误：backend目录缺失requirements.txt文件
    pause
    exit /b 1
)
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo 首次运行，自动安装依赖包
    pip install -r requirements.txt
)

echo [3/3] 启动FastAPI后端服务
echo.
echo 本地访问地址：http://localhost:8000
echo 接口文档地址：http://localhost:8000/docs
echo 按下 Ctrl+C 即可停止服务
echo ========================================
echo.

if not exist "main.py" (
    echo 错误：backend文件夹内缺少main.py主程序！
    pause
    exit /b 1
)
python main.py
pause