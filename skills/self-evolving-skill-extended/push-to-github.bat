@echo off
REM GitHub 推送脚本

echo ========================================
echo sessions_yield - GitHub 推送脚本
echo ========================================
echo.

REM 检查 Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未安装 Git，请先安装 Git
    echo 下载地址：https://git-scm.com/
    pause
    exit /b 1
)

echo [1/5] 初始化 Git 仓库...
git init

echo [2/5] 添加所有文件...
git add .

echo [3/5] 提交更改...
git commit -m "Initial commit: sessions_yield v1.0.0"

echo.
echo [4/5] 请输入您的 GitHub 仓库地址:
echo 格式：https://github.com/YOUR_USERNAME/sessions-yield.git
echo.
set /p REPO_URL="仓库地址："

if "%REPO_URL%"=="" (
    echo [错误] 未输入仓库地址
    pause
    exit /b 1
)

echo 添加远程仓库...
git remote add origin %REPO_URL%

echo.
echo [5/5] 推送到 GitHub...
echo 注意：首次推送需要输入 GitHub 用户名和密码
echo.
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo [成功] 推送完成！
    echo ========================================
    echo.
    echo 下一步:
    echo 1. 访问您的 GitHub 仓库
    echo 2. 完善 README.md 中的作者信息
    echo 3. 添加 GitHub Topics
    echo 4. 启用 GitHub Issues
    echo.
) else (
    echo.
    echo ========================================
    echo [失败] 推送失败，请检查:
    echo 1. 仓库地址是否正确
    echo 2. GitHub 账号是否登录
    echo 3. 是否有仓库写入权限
    echo ========================================
)

pause
