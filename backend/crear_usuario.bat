@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Primero ejecuta iniciar_backend.bat para instalar dependencias.
 pause
 exit /b 1
)
if not exist ".env" (
 ".venv\Scripts\python.exe" configurar.py
)
set "PYTHONPATH=%CD%\src"
echo REGISTRAR USUARIO ECOGESTION
".venv\Scripts\python.exe" -m backend.seed
pause
