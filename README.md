# Bible Verse Finder

A desktop application for searching, saving, and exporting Bible verses from the English Standard Version (ESV).

## Features
- Search Bible verses by topic
- Random topic suggestions
- Save favorite verses
- Export verses to PDF or TXT
- Right-click context menu
- Search history
- Modern, user-friendly interface

## Installation

### Option 1: Quick Install (Windows)
1. Download `install.bat` from the [releases page](https://github.com/kinglunalilo/BibleVerseFinder/releases)
2. Double-click to run the installer
3. Follow the on-screen instructions

The installer will:
- Check for/install Python 3.11.4
- Download required files
- Install dependencies
- Create a desktop shortcut

### Option 2: Git Clone (For Developers)
If you have Git installed:

1. Ensure Python 3.11.4 or higher is installed
2. Clone the repository:
   ```
   git clone https://github.com/kinglunalilo/BibleVerseFinder.git
   ```
3. Navigate to the project directory:
   ```
   cd BibleVerseFinder
   ```
4. Create an empty `resources/favorites.json` file with content: `[]`
5. Install required packages:
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