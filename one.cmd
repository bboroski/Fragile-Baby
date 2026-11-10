@echo off
setlocal
python "%~dp0one.py" %*
exit /b %errorlevel%
