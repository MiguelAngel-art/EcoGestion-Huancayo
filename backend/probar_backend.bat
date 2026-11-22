@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Primero ejecuta iniciar_backend.bat para instalar dependencias.
 pause
 exit /b 1
)
set "PYTHONPATH=%CD%\src"
".venv\Scripts\python.exe" -m pytest -q
pause
