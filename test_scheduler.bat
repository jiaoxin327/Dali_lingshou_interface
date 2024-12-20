# 创建 test_scheduler.bat
@echo off
chcp 65001 > nul
echo [测试模式] 零售数据上报系统

echo [%date% %time%] 检查并安装依赖...
pip install schedule

if not exist logs mkdir logs
echo [%date% %time%] 开始测试定时任务...
python scheduler.py
pause