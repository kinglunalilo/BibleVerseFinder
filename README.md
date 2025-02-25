# Bible Verse Finder

A simple tool to search, save, and export Bible verses.

## Installation Options

### Option 1: Automatic Installation (Recommended)
1. Download `install.bat`
2. Double-click to run the installer
3. Follow the on-screen instructions

The installer will:
- Install Python 3.11.4 if needed
- Download all required files
- Install necessary Python packages
- Create a desktop shortcut

### Option 2: Manual Installation
If you prefer to manually set up the program:

1. Ensure Python 3.11.4 or higher is installed
2. Download these required files:
   - search_scraper.py
   - start.vbs
   - __init__.py
3. Create an empty `resources/favorites.json` file with content: `[]`
4. Install required packages:
   ```
   pip install requests beautifulsoup4 pyperclip fpdf2 pillow
   ```

## Required Files
- search_scraper.py - Main program file
- start.vbs - Program launcher
- __init__.py - Package initialization
- resources/favorites.json - Saves your favorite verses
- resources/qr.png - Venmo QR code

## Directory Structure
```