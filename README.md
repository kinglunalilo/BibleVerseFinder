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
```
BibleVerseFinder/
├── search_scraper.py   # Main program file
├── start.vbs          # Program launcher
├── __init__.py       # Package initialization
├── install.bat       # Installation script
├── LICENSE          # MIT license with donation clause
└── resources/
    ├── favorites.json   # Saved verses
    ├── error_log.txt   # Application logs
    └── qr.png          # Donation QR code
```

## Usage
1. Launch the application using the desktop shortcut or `start.vbs`
2. Type a topic in the search box (e.g., "love", "faith", "hope")
3. Click "Search" or press Enter
4. Right-click on verses to:
   - Copy verse text
   - Save to favorites
   - Export to PDF/TXT

## Support Development
If you find this tool helpful, consider supporting its development:

- Scan the QR code below or in the app's About section
- Visit my [Venmo profile](https://venmo.com/lilow)
- Share the app with others

![Venmo QR Code](resources/qr.png)

Thank you for your support! 🙏 Your donation helps keep this project alive.

## Roadmap 🛣️
Future development will focus on deeper biblical understanding:

### Planned Features
- Windows executable for easier installation
- Tools for studying complex biblical topics:
  - End times prophecies
  - Biblical mysteries
  - Difficult passages explained
  - Revelation study aids
  - Greek word interpretations
  - Cross-reference analysis
- Advanced search capabilities
- Mobile version (future)

Stay tuned and ⭐ star the repository for updates!

## License
This project is licensed under the MIT License with an additional clause regarding donations - see the [LICENSE](LICENSE) file for details.