@echo off
REM Lo ejecuta el Programador de tareas. Corre sin ventana y reintenta ~50 min.
REM Estos valores tienen prioridad sobre los del .env.
cd /d "%~dp0"
set HEADLESS=true
set INTENTOS=25
set ESPERA_SEG=120
set PYTHONIOENCODING=utf-8
echo. >> log.txt
echo ===== %date% %time% ===== >> log.txt
python asistencia.py >> log.txt 2>&1
