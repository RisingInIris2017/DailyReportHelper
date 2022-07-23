@echo off
echo 程序将在五秒后打印登录二维码，
echo 请将窗口最大化以免扫码失败！
TIMEOUT /T 5
python.exe ".\DailyReportHelper.py"
pause