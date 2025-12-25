@echo off
REM OpenAgents Network Auto Start Script

REM Set project path
SET PROJECT_PATH=C:\Users\biren\Documents\trae_projects\ai

REM Change to project directory
cd /d %PROJECT_PATH%

REM Activate virtual environment
echo Activating virtual environment...
call %PROJECT_PATH%\openagents_env\Scripts\activate.bat

REM Start OpenAgents network
echo Starting OpenAgents network...
openagents network start ./learning_assistant_network/network.yaml

REM Wait for network to start
ping 127.0.0.1 -n 5 > nul

REM Start learning assistant agent
python ./my_first_network/agents/learning_assistant_agent.py