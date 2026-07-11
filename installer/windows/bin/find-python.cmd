@echo off
setlocal EnableExtensions

set "NOVADEV_PYTHON_CMD="
set "NOVADEV_PYTHON_EXE="

py -3 -c "import sys, tkinter; print(sys.version)" >nul 2>nul
if not errorlevel 1 (
    endlocal & set "NOVADEV_PYTHON_CMD=py -3" & exit /b 0
)

python -c "import sys, tkinter; print(sys.version)" >nul 2>nul
if not errorlevel 1 (
    endlocal & set "NOVADEV_PYTHON_CMD=python" & exit /b 0
)

python3 -c "import sys, tkinter; print(sys.version)" >nul 2>nul
if not errorlevel 1 (
    endlocal & set "NOVADEV_PYTHON_CMD=python3" & exit /b 0
)

for /f "delims=" %%P in ('where python 2^>nul') do (
    "%%P" -c "import sys, tkinter; print(sys.version)" >nul 2>nul
    if not errorlevel 1 (
        endlocal & set "NOVADEV_PYTHON_EXE=%%P" & exit /b 0
    )
)

for /f "delims=" %%P in ('where py 2^>nul') do (
    "%%P" -3 -c "import sys, tkinter; print(sys.version)" >nul 2>nul
    if not errorlevel 1 (
        endlocal & set "NOVADEV_PYTHON_CMD=py -3" & exit /b 0
    )
)

echo NovaDev could not find a Python 3 install with tkinter.
echo Install Python from https://www.python.org/downloads/windows/ and make sure Tcl/Tk is enabled.
endlocal & exit /b 1
