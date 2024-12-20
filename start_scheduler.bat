@echo off
chcp 65001 > nul
title 零售数据上报系统[后台运行]

echo [生产模式] 零售数据上报系统
echo 时间: %date% %time%

:: 检查并创建日志目录
if not exist logs mkdir logs

:: 检查依赖
echo 检查依赖...
pip install schedule > nul

:: 检查是否已经在运行
tasklist /FI "IMAGENAME eq pythonw.exe" | find "pythonw.exe" > nul
if %ERRORLEVEL% EQU 0 (
    echo 警告: 系统中已有 pythonw.exe 进程在运行
    echo 请确认是否重复启动
    choice /C YN /M "是否继续启动?"
    if errorlevel 2 goto :end
)

:: 启动后台进程
echo 启动后台任务...
start /b pythonw scheduler.py > logs/scheduler.log 2>&1

:: 等待确认进程启动
timeout /t 3 > nul
tasklist /FI "IMAGENAME eq pythonw.exe" | find "pythonw.exe" > nul
if %ERRORLEVEL% EQU 0 (
    echo 后台任务已成功启动
    echo 日志文件位置: logs/scheduler.log
) else (
    echo 警告: 后台任务可能未正常启动
    echo 请检查日志文件
)

echo.
echo 提示:
echo 1. 使用 stop_scheduler.bat 可以停止程序
echo 2. 使用任务管理器查看 pythonw.exe 进程
echo 3. 通过 logs/scheduler.log 查看运行日志
echo.

timeout /t 5

:end