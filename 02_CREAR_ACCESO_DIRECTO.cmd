@echo off
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0APP\crear_acceso_directo.ps1"
pause
