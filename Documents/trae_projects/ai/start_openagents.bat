@echo off
REM OpenAgents网络服务自动启动脚本
REM 作者: AI Assistant
REM 日期: %date%

REM 检查是否以管理员身份运行
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo 请以管理员身份运行此脚本！
    pause
    exit /b 1
)

REM 设置项目路径
SET PROJECT_PATH=C:\Users\biren\Documents\trae_projects\ai

REM 切换到项目目录
cd /d %PROJECT_PATH%

REM 检查虚拟环境是否存在
IF NOT EXIST "%PROJECT_PATH%\openagents_env" (
    echo 虚拟环境不存在，请先创建虚拟环境！
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 正在激活虚拟环境...
call %PROJECT_PATH%\openagents_env\Scripts\activate.bat

REM 检查OpenAgents是否已安装
pip show openagents >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo OpenAgents未安装，正在安装...
    pip install -r requirements.txt
)

REM 启动OpenAgents网络服务
echo 正在启动OpenAgents网络服务...
echo 服务将在新窗口中启动，请勿关闭该窗口。
start "OpenAgents Network Server" cmd /k "openagents network start ./my_first_network/network.yaml"

REM 等待服务启动
echo 正在等待服务启动...
timeout /t 5 /nobreak

REM 检查服务是否正常运行
echo 正在检查服务状态...
curl http://localhost:8700/api/health >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo 服务启动成功！可通过 http://localhost:8700 访问
) ELSE (
    echo 服务启动可能失败，请检查网络配置和日志。
)

echo 启动脚本执行完成！
pause
