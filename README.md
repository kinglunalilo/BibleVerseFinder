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
3. Create an empty `favorites.json` file with content: `[]`
4. Install required packages:
   ```
   pip install requests beautifulsoup4 pyperclip fpdf2 pillow
   ```

## Required Files
- search_scraper.py - Main program file
- start.vbs - Program launcher
- __init__.py - Package initialization
- favorites.json - Saves your favorite verses

## Running the Program
- Use the desktop shortcut (if installed with Option 1)
- OR double-click `start.vbs`

## Features
- Search Bible verses
- Save favorite verses
- Export verses to PDF
- Copy verses to clipboard
- Simple VBS interface

## Troubleshooting
- If the program won't start, ensure Python is in your system PATH
- Check that all required packages are installed
- Verify all files are in the same directory

## Support the Project
If you find this tool helpful, consider supporting its development:

- Venmo: @lilow
- Or scan the QR code in the program's About dialog

## Requirements
- Windows 7 or higher
- Python 3.11.4 or higher
- Internet connection for verse searches
- 50MB free disk space

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support
For issues or questions, please open an issue in this repository.

## Support the Developer

If you find this application helpful and would like to support its development, you can donate through Venmo:

![Venmo QR Code](qr.png)

Or visit: [https://venmo.com/lilow](https://venmo.com/lilow)

Your support helps maintain and improve this application. Thank you! 🙏