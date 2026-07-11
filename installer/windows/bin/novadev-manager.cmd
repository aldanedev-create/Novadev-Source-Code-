@echo off
setlocal EnableExtensions

for %%I in ("%~dp0..") do set "NOVADEV_HOME=%%~fI"
set "NOVADEV_LANGUAGE=%NOVADEV_HOME%\language"
set "NOVADEV_MANAGER=%NOVADEV_LANGUAGE%\novadev_manager.py"
set "NOVADEV_LOG_DIR=%NOVADEV_HOME%\logs"
set "NOVADEV_LOG=%NOVADEV_LOG_DIR%\manager.log"

if not exist "%NOVADEV_LOG_DIR%" mkdir "%NOVADEV_LOG_DIR%" >nul 2>nul

echo [%date% %time%] Starting NovaDev Manager > "%NOVADEV_LOG%"
echo [%date% %time%] Home: %NOVADEV_HOME% >> "%NOVADEV_LOG%"
echo [%date% %time%] Language: %NOVADEV_LANGUAGE% >> "%NOVADEV_LOG%"

if not exist "%NOVADEV_MANAGER%" (
    echo [%date% %time%] Missing manager file: %NOVADEV_MANAGER% >> "%NOVADEV_LOG%"
    echo NovaDev Manager is missing. See "%NOVADEV_LOG%"
    exit /b 10
)

call "%~dp0find-python.cmd" >> "%NOVADEV_LOG%" 2>&1
if errorlevel 1 (
    echo [%date% %time%] Python with tkinter was not found. >> "%NOVADEV_LOG%"
    echo Python with tkinter was not found. See "%NOVADEV_LOG%"
    exit /b 11
)

if defined NOVADEV_PYTHON_EXE (
    echo [%date% %time%] Using Python executable: %NOVADEV_PYTHON_EXE% >> "%NOVADEV_LOG%"
    "%NOVADEV_PYTHON_EXE%" "%NOVADEV_MANAGER%" %* >> "%NOVADEV_LOG%" 2>&1
) else (
    echo [%date% %time%] Using Python command: %NOVADEV_PYTHON_CMD% >> "%NOVADEV_LOG%"
    %NOVADEV_PYTHON_CMD% "%NOVADEV_MANAGER%" %* >> "%NOVADEV_LOG%" 2>&1
)

set "EXIT_CODE=%errorlevel%"
echo [%date% %time%] NovaDev Manager exited with %EXIT_CODE%. >> "%NOVADEV_LOG%"
if not "%EXIT_CODE%"=="0" (
    echo NovaDev Manager failed. See "%NOVADEV_LOG%"
)

exit /b %EXIT_CODE%
