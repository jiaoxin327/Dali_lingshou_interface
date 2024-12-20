@echo off
chcp 65001 > nul
title 零售数据上报系统[停止程序]

echo [%date% %time%] 正在停止零售数据上报系统...

:: 查找并停止 pythonw.exe 进程
tasklist /FI "IMAGENAME eq pythonw.exe" | find "pythonw.exe" > nul
if %ERRORLEVEL% EQU 0 (
    echo 找到运行中的程序
    echo 进程信息:
    tasklist /FI "IMAGENAME eq pythonw.exe"
    echo.
    choice /C YN /M "确认要停止程序吗?"
    if errorlevel 2 (
        echo 操作已取消
        goto :end
    )
    
    echo 正在停止程序...
    taskkill /F /IM pythonw.exe
    if %ERRORLEVEL% EQU 0 (
        echo [%date% %time%] 程序已成功停止
        :: 记录停止操作到日志（使用UTF-8编码）
        powershell -Command "Add-Content -Path logs/scheduler.log -Value '[%date% %time%] 系统被手动停止' -Encoding UTF8"
    ) else (
        echo 停止程序时出错，请手动检查任务管理器
    )
) else (
    echo 未发现运行中的程序
)

echo.
echo 提示:
echo 1. 请检查任务管理器确认 pythonw.exe 已停止
echo 2. 可以查看 logs/scheduler.log 了解运行历史
echo.

:end
pause 