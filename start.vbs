Set objShell = CreateObject("WScript.Shell") 
objShell.CurrentDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) 
objShell.Run "pythonw search_scraper.py", 0, False 
