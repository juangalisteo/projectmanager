@echo off
setlocal
chcp 65001 >nul
title Project Manager
where python >nul 2>&1
if errorlevel 1 (
 echo No se encuentra Python. Instala Python 3 desde python.org y vuelve a abrir este archivo.
 pause
 exit /b 1
)
where pythonw >nul 2>&1
if errorlevel 1 goto ventana
start "" pythonw -s "%~dp0APP\interfaz.py"
exit /b 0
:ventana
python -s "%~dp0APP\interfaz.py"
if errorlevel 1 pause
