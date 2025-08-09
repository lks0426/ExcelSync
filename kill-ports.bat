@echo off
chcp 65001 >nul
title ExcelSync 端口清理工具

echo 🔄 开始清理 ExcelSync 相关端口...
echo ========================================

REM 定义要清理的端口
set PORTS=3000 3001 8000 8001

for %%p in (%PORTS%) do (
    echo 🔍 检查端口 %%p...
    
    REM 查找占用端口的进程
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%p') do (
        if not "%%a"=="0" (
            echo ❌ 端口 %%p 正在被进程 %%a 使用，正在关闭...
            taskkill /PID %%a /F >nul 2>&1
            if not errorlevel 1 (
                echo ✅ 端口 %%p 已成功关闭
            ) else (
                echo ⚠️  无法关闭端口 %%p 上的进程 %%a
            )
        )
    )
    
    REM 如果没有找到进程，说明端口可用
    netstat -aon | findstr :%%p >nul 2>&1
    if errorlevel 1 (
        echo ✅ 端口 %%p 已经可用
    )
)

echo ========================================
echo 🎉 端口清理完成！
echo.
echo 端口状态：

for %%p in (%PORTS%) do (
    netstat -aon | findstr :%%p >nul 2>&1
    if errorlevel 1 (
        echo   端口 %%p: ✅ 可用
    ) else (
        echo   端口 %%p: ❌ 仍在使用
    )
)

echo.
echo 💡 提示：
echo   - 前端启动: cd frontend ^&^& npm run dev
echo   - 后端启动: cd backend ^&^& python app.py
echo.
pause