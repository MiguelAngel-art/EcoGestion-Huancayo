@echo off
setlocal
cd /d "%~dp0"
echo =============================
echo  ECOGESTION HUANCAYO - API
echo =============================
where py >nul 2>nul
if errorlevel 1 (
  echo Python no se encontro con el comando py. Instala Python 3.11 o superior.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Creando entorno virtual...
  py -m venv .venv
  if errorlevel 1 goto error
)
echo [2/3] Instalando dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error
if not exist ".env" (
  ".venv\Scripts\python.exe" configurar.py
  if errorlevel 1 goto error
)
echo [3/3] Iniciando en http://127.0.0.1:8000/docs
echo Para detener: Ctrl + C
".venv\Scripts\python.exe" -m uvicorn backend.main:app --app-dir src --reload --host 127.0.0.1 --port 8000
exit /b %errorlevel%
:error
echo ERROR: Revisa el mensaje anterior.
pause
exit /b 1
