@echo off
setlocal
for %%I in ("%~dp0..") do set "NOVADEV_HOME=%%~fI"
call "%~dp0find-python.cmd"
if errorlevel 1 exit /b 1
%NOVADEV_PYTHON% "%NOVADEV_HOME%\language\shell.py" %*
exit /b %errorlevel%
