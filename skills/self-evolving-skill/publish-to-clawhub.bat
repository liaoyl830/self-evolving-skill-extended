@echo off
REM ClawHub 发布脚本

echo ========================================
echo sessions_yield - ClawHub 发布脚本
echo ========================================
echo.

REM 检查 clawhub
npx clawhub --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未安装 clawhub，请先安装
    echo 运行：npm install -g clawhub
    pause
    exit /b 1
)

echo [1/3] 检查 claw.json...
if not exist claw.json (
    echo [错误] claw.json 不存在
    pause
    exit /b 1
)
echo   ✓ claw.json 存在

echo.
echo [2/3] 登录 ClawHub...
echo 如果没有账号，请先访问 https://clawhub.ai 注册
echo.
npx clawhub login

if %errorlevel% neq 0 (
    echo [错误] 登录失败
    pause
    exit /b 1
)

echo.
echo [3/3] 发布技能到 ClawHub...
echo.
npx clawhub publish .

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo [成功] 发布完成！
    echo ========================================
    echo.
    echo 下一步:
    echo 1. 访问 https://clawhub.ai
    echo 2. 搜索 "sessions-yield"
    echo 3. 查看技能详情页
    echo 4. 分享安装链接
    echo.
    echo 安装命令:
    echo npx clawhub add YOUR_USERNAME/sessions-yield
    echo.
) else (
    echo.
    echo ========================================
    echo [失败] 发布失败，请检查:
    echo 1. claw.json 配置是否正确
    echo 2. ClawHub 账号是否登录
    echo 3. 技能名称是否已被占用
    echo ========================================
)

pause
