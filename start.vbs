Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get full paths
strCurrentDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
strResourcesDir = objFSO.BuildPath(strCurrentDir, "resources")
strLogFile = objFSO.BuildPath(strResourcesDir, "error_log.txt")

' Create log function
Sub LogError(strMessage)
    Set objFile = objFSO.OpenTextFile(strLogFile, 8, True)
    objFile.WriteLine Now & " - " & strMessage
    objFile.Close
End Sub

' Ensure resources directory exists
If Not objFSO.FolderExists(strResourcesDir) Then
    objFSO.CreateFolder(strResourcesDir)
End If

' Change to script directory
objShell.CurrentDirectory = strCurrentDir

' Create empty favorites.json if it doesn't exist
strFavoritesPath = objFSO.BuildPath(strResourcesDir, "favorites.json")
If Not objFSO.FileExists(strFavoritesPath) Then
    Set objFile = objFSO.OpenTextFile(strFavoritesPath, 2, True)
    objFile.Write "[]"
    objFile.Close
End If

' Check if Python is installed
Function IsPythonInstalled()
    On Error Resume Next
    objShell.Run "python --version", 0, True
    IsPythonInstalled = (Err.Number = 0)
    On Error Goto 0
End Function

' Final launch section with enhanced error handling
On Error Resume Next
If Not IsPythonInstalled() Then
    LogError "Python not found in system PATH"
    objShell.Popup "Python is not installed or not in system PATH. Please install Python 3.x and try again.", 0, "Error", 16
    WScript.Quit
End If

Dim launchSuccess : launchSuccess = False

' Try pythonw first
objShell.Run "pythonw " & Chr(34) & objFSO.BuildPath(strCurrentDir, "search_scraper.py") & Chr(34), 0, False
If Err.Number = 0 Then
    launchSuccess = True
Else
    LogError "Failed to launch with pythonw: " & Err.Description
    Err.Clear
    
    ' Try python as fallback
    objShell.Run "python " & Chr(34) & objFSO.BuildPath(strCurrentDir, "search_scraper.py") & Chr(34), 0, False
    If Err.Number = 0 Then
        launchSuccess = True
    Else
        LogError "Failed to launch with python: " & Err.Description
        objShell.Popup "Error starting the program. Check error_log.txt in the resources folder for details.", 0, "Error", 16
    End If
End If

If launchSuccess Then
    LogError "Application launched successfully"
End If
