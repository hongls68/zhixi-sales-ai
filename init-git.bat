@echo off
chcp 65001 >nul
echo ========================================
echo   智析销售AI - Git初始化脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/6] 检查Git是否安装...
git --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Git，请先安装Git
    echo 下载地址：https://git-scm.com/downloads
    pause
    exit /b 1
)
echo Git已安装

echo.
echo [2/6] 初始化Git仓库...
if exist ".git" (
    echo .git目录已存在，跳过初始化
) else (
    git init
    git branch -m main
)

echo.
echo [3/6] 配置Git用户信息...
set /p GIT_EMAIL="请输入你的GitHub邮箱（直接回车使用默认）: "
if "%GIT_EMAIL%"=="" set GIT_EMAIL=hongls68@users.noreply.github.com
git config user.email "%GIT_EMAIL%"
git config user.name "hongls68"
echo 已配置：%GIT_EMAIL%

echo.
echo [4/6] 添加远程仓库...
git remote remove origin 2>nul
git remote add origin https://github.com/hongls68/zhixi-sales-ai.git
echo 已添加远程仓库

echo.
echo [5/6] 添加文件并提交...
git add .
git status --short
echo.
set /p CONFIRM="确认提交以上文件？(Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo 已取消
    pause
    exit /b 0
)
git commit -m "v1.2: 交互优化+功能补全 - Toast、动画、搜索筛选、分页组件"

echo.
echo [6/6] 推送到GitHub...
echo 注意：首次推送需要输入GitHub用户名和密码/Token
git push -u origin main

echo.
echo ========================================
echo   完成！
echo ========================================
echo.
echo 后续版本提交命令：
echo   git add .
echo   git commit -m "v1.x: 更新说明"
echo   git push
echo.
echo 创建版本标签：
echo   git tag -a v1.2 -m "v1.2: 交互优化+功能补全"
echo   git push origin v1.2
echo.
pause
