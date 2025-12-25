@echo off

REM 学习助理网络启动脚本
REM 基于 OpenAgents 平台

echo 正在启动学习助理网络...
echo.

REM 检查是否已经激活虚拟环境
if not defined VIRTUAL_ENV (
    echo 请先激活虚拟环境！
    echo 例如: openagents_env\Scripts\activate
    pause
    exit /b 1
)

echo 当前目录: %cd%
echo.

REM 启动学习助理网络
echo 正在启动学习助理网络...
cd learning_assistant_network
python -m openagents network start

cd ..
echo.
echo 学习助理网络已启动！
pause