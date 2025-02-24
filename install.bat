@echo off
setlocal EnableDelayedExpansion
set "LOG_FILE=install.log"
set "PYTHON_VERSION=3.11.4"
set "PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe"
set "INSTALL_DIR=BibleVerseFinder"
set "GITHUB_BASE=https://raw.githubusercontent.com/kinglunalilo/BibleVerseFinder/main"
set "REPO_URL=https://github.com/kinglunalilo/BibleVerseFinder.git"

REM Quick Python check before anything else
set "PYTHON_FOUND=0"
python --version >nul 2>&1 && set "PYTHON_FOUND=1"
if not "%PYTHON_FOUND%"=="1" py --version >nul 2>&1 && set "PYTHON_FOUND=1"
if not "%PYTHON_FOUND%"=="1" if exist "C:\Python311\python.exe" set "PATH=C:\Python311;%PATH%" && set "PYTHON_FOUND=1"
if not "%PYTHON_FOUND%"=="1" if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PATH=%LOCALAPPDATA%\Programs\Python\Python311;%PATH%" && set "PYTHON_FOUND=1"

cls
echo ============================================
echo    Bible Verse Finder Setup
echo ============================================
echo.

REM Check if program is already installed
if exist "%INSTALL_DIR%\start.vbs" (
    echo Bible Verse Finder is already installed!
    echo.
    echo To run the program, please use:
    echo  - The desktop shortcut, or
    echo  - Double-click start.vbs in the BibleVerseFinder folder
    echo.
    echo You don't need to run this installer again.
    echo.
    pause
    exit /b 0
)

echo Checking system requirements...
if "%PYTHON_FOUND%"=="1" (
    echo Python %PYTHON_VERSION% is already installed.
    echo.
    echo Ready to install Bible Verse Finder:
    echo  1. Download required program files
    echo  2. Install necessary Python packages
    echo  3. Create a desktop shortcut
) else (
    echo Python %PYTHON_VERSION% needs to be installed.
    echo.
    echo Installation steps:
    echo  1. Install Python %PYTHON_VERSION% ^(approximately 25MB^)
    echo  2. Download required program files
    echo  3. Install necessary Python packages
    echo  4. Create a desktop shortcut
)
echo.
echo Note: Internet connection is required
echo.
echo Press any key to begin...
pause >nul

echo ===== Bible Verse Finder Installation ===== > %LOG_FILE%
echo %DATE% %TIME% - Starting installation... >> %LOG_FILE%

if "%PYTHON_FOUND%"=="1" goto :install_app

REM Install Python if not found
echo Installing Python %PYTHON_VERSION%...
echo.
curl -L -# "https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%" --output "%PYTHON_INSTALLER%" || goto :error
echo Starting Python installation... Please wait...
echo This may take a few minutes. Do not close this window.
start /wait "" "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1
echo Python installation in progress... Please wait...
timeout /t 5 /nobreak >nul
del /f /q "%PYTHON_INSTALLER%"

echo.
echo Python installation completed!
echo ============================================
echo IMPORTANT: Please run this installer again
echo to complete the Bible Verse Finder setup.
echo ============================================
echo.
pause
exit /b 0

:install_app
REM Create installation directories
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\resources" mkdir "%INSTALL_DIR%\resources"
cd "%INSTALL_DIR%"

REM Download main program files
echo Downloading program files...
where git >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Using Git to download files...
    git clone "%REPO_URL%" . || goto :direct_download
) else (
    :direct_download
    echo Using direct file download...
    REM Download main program files to root directory
    for %%f in (search_scraper.py start.vbs __init__.py) do (
        echo Downloading %%f...
        powershell -Command "& {try { $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri '%GITHUB_BASE%/%%f' -OutFile '%%f' -UseBasicParsing } catch { exit 1 }}"
        if not exist "%%f" (
            echo Retrying with curl...
            curl -L -f -s "%GITHUB_BASE%/%%f" --output "%%f"
            if not exist "%%f" (
                echo Failed to download %%f
                echo Last error code: !ERRORLEVEL!
                goto :error
            )
        )
    )
    
    REM Download resource files to resources directory
    cd resources
    for %%f in (qr.png) do (
        echo Downloading %%f to resources folder...
        powershell -Command "& {try { $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri '%GITHUB_BASE%/resources/%%f' -OutFile '%%f' -UseBasicParsing } catch { exit 1 }}"
        if not exist "%%f" (
            echo Retrying with curl...
            curl -L -f -s "%GITHUB_BASE%/resources/%%f" --output "%%f"
        )
    )
    
    REM Create empty favorites.json in resources if it doesn't exist
    if not exist "favorites.json" echo [] > "favorites.json"
    cd ..
)

REM Verify downloads
echo Verifying downloaded files...
for %%f in (search_scraper.py start.vbs __init__.py) do (
    if not exist "%%f" (
        echo Missing required file: %%f
        goto :error
    )
)

REM Create favorites.json if needed
if not exist "favorites.json" echo [] > favorites.json

REM Install Python packages
echo Installing required packages...
python -m pip install --no-cache-dir requests beautifulsoup4 pyperclip fpdf2 pillow || goto :error

REM Create desktop shortcut
echo Creating desktop shortcut...
(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set lnk = WshShell.CreateShortcut^(WshShell.SpecialFolders^("Desktop"^) ^& "\Bible Verse Finder.lnk"^)
    echo lnk.TargetPath = WshShell.CurrentDirectory ^& "\start.vbs"
    echo lnk.WorkingDirectory = WshShell.CurrentDirectory
    echo lnk.Save
) > CreateShortcut.vbs
cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

echo.
echo Installation complete! Use the desktop shortcut or start.vbs to run the program.
goto :end

:error
echo.
echo ERROR: Installation failed.
echo Last error code: %ERRORLEVEL%
echo Current directory: %CD%
echo.
echo Details:
type %LOG_FILE% 2>nul
echo.
pause
exit /b 1

:end
echo %DATE% %TIME% - Installation completed successfully >> %LOG_FILE%
echo.
echo ============================================
echo Installation complete! 
echo.
echo To run Bible Verse Finder:
echo  1. Use the desktop shortcut, or
echo  2. Double-click start.vbs in the BibleVerseFinder folder
echo.
echo You won't need to run this installer again.
echo ============================================
echo.
pause
exit /b 0