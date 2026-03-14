@echo off
REM 快速配置脚本

echo ========================================
echo sessions_yield - 快速配置
echo ========================================
echo.
echo 请设置以下信息 (用于 GitHub 和 ClawHub):
echo.

set /p AUTHOR_NAME="作者名称 (例如：YourName 或 GitHub ID): "
set /p GITHUB_USER="GitHub 用户名: "
set /p GITHUB_REPO="GitHub 仓库地址 (完整 URL): "

if "%AUTHOR_NAME%"=="" (
    echo [错误] 作者名称不能为空
    pause
    exit /b 1
)

if "%GITHUB_USER%"=="" (
    echo [错误] GitHub 用户名不能为空
    pause
    exit /b 1
)

echo.
echo [1/3] 更新 README.md...
powershell -Command "(Get-Content README.md) -replace 'YOUR_NAME', '%AUTHOR_NAME%' -replace 'YOUR_USERNAME', '%GITHUB_USER%' | Set-Content README.md"
echo   ✓ README.md 已更新

echo [2/3] 更新 claw.json...
powershell -Command "(Get-Content claw.json) -replace 'YOUR_NAME', '%AUTHOR_NAME%' -replace 'YOUR_USERNAME', '%GITHUB_USER%' | Set-Content claw.json"
echo   ✓ claw.json 已更新

echo [3/3] 更新 LICENSE...
powershell -Command "(Get-Content LICENSE) -replace 'YOUR_NAME', '%AUTHOR_NAME%' | Set-Content LICENSE"
echo   ✓ LICENSE 已更新

echo.
echo ========================================
echo [完成] 配置已更新！
echo ========================================
echo.
echo 作者：%AUTHOR_NAME%
echo GitHub: %GITHUB_USER%
echo 仓库：%GITHUB_REPO%
echo.
echo 下一步:
echo 1. 运行 push-to-github.bat 推送到 GitHub
echo 2. 运行 publish-to-clawhub.bat 发布到 ClawHub
echo.

pause
