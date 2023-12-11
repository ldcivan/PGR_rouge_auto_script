@echo off
title GenshinAssistant
mode con: cols=50
set curdir=%~dp0
cd /d %curdir%
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Administrator permissions got.
    goto :admin
) else (
    echo Administrator permissions required. Right-click and select "Run as administrator".
    pause >nul
    exit
)

:admin

REM 检测是否已安装 Python
echo Checking......Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Please install Python first
    exit /b
)

echo Python and requirements has been installed. Now running main script...

:start
python main.py

pause
goto start