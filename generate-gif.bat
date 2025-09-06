@echo off
REM Discord Logo GIF Generator - Windows Batch Script
REM Vereinfachtes Interface für die GIF-Erstellung

setlocal enabledelayedexpansion

REM Funktionen simulieren mit Labels
if "%1"=="" goto :help
if "%1"=="help" goto :help
if "%1"=="-h" goto :help
if "%1"=="--help" goto :help
if "%1"=="discord" goto :discord
if "%1"=="discord-small" goto :discord-small
if "%1"=="discord-large" goto :discord-large
if "%1"=="banner" goto :banner
if "%1"=="custom" goto :custom
if "%1"=="watch" goto :watch
if "%1"=="list" goto :list

echo ❌ Unbekannte Option: %1
echo.
goto :help

:header
echo 🎬 Discord Logo GIF Generator
echo ==================================
echo.
goto :eof

:check_python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python ist nicht installiert oder nicht im PATH!
    echo Bitte installiere Python 3 von https://python.org
    exit /b 1
)

python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Pillow nicht gefunden, installiere...
    pip install --user pillow
)
goto :eof

:discord
call :header
call :check_python
echo ℹ️ Erstelle Standard Discord GIF (512px)...
python generate-discord-gif.py discord
if errorlevel 1 (
    echo ❌ Fehler bei der GIF-Erstellung!
    exit /b 1
)
echo ✅ GIF erfolgreich erstellt!
goto :show_result

:discord-small
call :header
call :check_python
echo ℹ️ Erstelle kleines Discord GIF (256px)...
python generate-discord-gif.py discord-klein
if errorlevel 1 (
    echo ❌ Fehler bei der GIF-Erstellung!
    exit /b 1
)
echo ✅ GIF erfolgreich erstellt!
goto :show_result

:discord-large
call :header
call :check_python
echo ℹ️ Erstelle großes Discord GIF (1024px)...
python generate-discord-gif.py discord-gross
if errorlevel 1 (
    echo ❌ Fehler bei der GIF-Erstellung!
    exit /b 1
)
echo ✅ GIF erfolgreich erstellt!
goto :show_result

:banner
call :header
call :check_python
echo ℹ️ Erstelle quadratisches Banner GIF...
python generate-discord-gif.py banner
if errorlevel 1 (
    echo ❌ Fehler bei der GIF-Erstellung!
    exit /b 1
)
echo ✅ GIF erfolgreich erstellt!
goto :show_result

:custom
call :header
call :check_python
echo ℹ️ Erstelle benutzerdefiniertes GIF...
python generate-discord-gif.py --custom --size 512 --glow medium
if errorlevel 1 (
    echo ❌ Fehler bei der GIF-Erstellung!
    exit /b 1
)
echo ✅ GIF erfolgreich erstellt!
goto :show_result

:watch
call :header
call :check_python
echo ℹ️ Starte Datei-Überwachung...
echo ⚠️ Drücke Ctrl+C zum Beenden
python generate-discord-gif.py discord --watch
goto :eof

:list
call :header
call :check_python
python generate-discord-gif.py --list
goto :eof

:show_result
if exist "assets\discord_logo.gif" (
    echo ℹ️ Speicherort: assets\discord_logo.gif
    dir "assets\discord_logo.gif" | find "discord_logo.gif"
)
goto :eof

:help
call :header
echo Verwendung: %0 [OPTION]
echo.
echo Optionen:
echo   discord          Standard Discord Icon (512px)
echo   discord-small    Kleines Discord Icon (256px)
echo   discord-large    Großes Discord Icon (1024px)
echo   banner           Quadratisches Banner
echo   custom           Benutzerdefinierte Einstellungen
echo   watch            Datei-Überwachung starten
echo   list             Verfügbare Presets anzeigen
echo   help             Diese Hilfe anzeigen
echo.
echo Beispiele:
echo   %0 discord       # Standard Discord GIF erstellen
echo   %0 watch         # Automatische Regenerierung
echo   %0 list          # Alle Presets anzeigen
echo.
echo Voraussetzungen:
echo   - Python 3 installiert
echo   - assets\logo.png vorhanden
goto :eof