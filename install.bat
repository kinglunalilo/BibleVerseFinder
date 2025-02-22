@echo off
echo ===== Bible Verse Finder Installation =====
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found in PATH
    echo Download from https://www.python.org/downloads/
    echo Remember to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Define file URLs (replace with actual URLs to your files)
set "SEARCH_SCRAPER_URL=https://example.com/path/to/search_scraper.py"
set "START_VBS_URL=https://example.com/path/to/start.vbs"
set "INIT_PY_URL=https://example.com/path/to/__init__.py"

REM Create the BibleVerseFinder folder
if not exist "BibleVerseFinder" mkdir "BibleVerseFinder"
cd "BibleVerseFinder"

REM Delete existing files (reset functionality)
echo Resetting existing installation...
del /q *.* >nul 2>&1

REM Download necessary files
echo Downloading program files...
powershell -Command "Invoke-WebRequest -Uri '%SEARCH_SCRAPER_URL%' -OutFile 'search_scraper.py'"
if errorlevel 1 (
    echo ERROR: Failed to download search_scraper.py
    pause
    exit /b 1
)

powershell -Command "Invoke-WebRequest -Uri '%START_VBS_URL%' -OutFile 'start.vbs'"
if errorlevel 1 (
    echo ERROR: Failed to download start.vbs
    pause
    exit /b 1
)

powershell -Command "Invoke-WebRequest -Uri '%INIT_PY_URL%' -OutFile '__init__.py'"
if errorlevel 1 (
    echo ERROR: Failed to download __init__.py
    pause
    exit /b 1
)

REM Create favorites.json if it doesn't exist
if not exist "favorites.json" echo [] > favorites.json

REM Install required Python packages
echo Installing required packages...
python -m pip install requests beautifulsoup4 pyperclip fpdf2 pillow
if errorlevel 1 (
    echo ERROR: Package installation failed
    pause
    exit /b 1
)

REM Create desktop shortcut
echo Creating desktop shortcut...
echo Set WshShell = CreateObject("WScript.Shell") > CreateShortcut.vbs
echo shortcut = WshShell.SpecialFolders("Desktop") ^& "\Bible Verse Finder.lnk" >> CreateShortcut.vbs
echo Set lnk = WshShell.CreateShortcut(shortcut) >> CreateShortcut.vbs
echo lnk.TargetPath = WshShell.CurrentDirectory ^& "\start.vbs" >> CreateShortcut.vbs
echo lnk.WorkingDirectory = WshShell.CurrentDirectory >> CreateShortcut.vbs
echo lnk.Save >> CreateShortcut.vbs
cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

echo Installation complete! Use the desktop shortcut or start.vbs to run the program.
pause 