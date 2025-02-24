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

' Check for Python updates
Set objHTTP = CreateObject("MSXML2.XMLHTTP")
strGitHubAPI = "https://api.github.com/repos/kinglunalilo/BibleVerseFinder/commits/main"
strGitHubRaw = "https://raw.githubusercontent.com/kinglunalilo/BibleVerseFinder/main/"

' Update check file should be in resources folder
strHashFile = objFSO.BuildPath(strResourcesDir, "last_commit.txt")
strLocalHash = ""

If objFSO.FileExists(strHashFile) Then
    Set objFile = objFSO.OpenTextFile(strHashFile, 1)
    strLocalHash = objFile.ReadLine()
    objFile.Close()
End If

' Check for updates
On Error Resume Next
objHTTP.Open "GET", strGitHubAPI, False
objHTTP.setRequestHeader "User-Agent", "BibleVerseFinder-UpdateChecker"
objHTTP.send

If objHTTP.Status = 200 Then
    strResponse = objHTTP.responseText
    intStart = InStr(strResponse, """sha"":""") + 8
    intEnd = InStr(intStart, strResponse, """") - 1
    strRemoteHash = Mid(strResponse, intStart, intEnd - intStart + 1)
    
    If strLocalHash <> strRemoteHash Then
        objShell.Popup "Updates found! Downloading latest version...", 2, "Bible Verse Finder Update", 64
        
        ' Update files
        For Each strFile in Array("search_scraper.py", "__init__.py")
            objHTTP.Open "GET", strGitHubRaw & strFile, False
            objHTTP.send
            
            If objHTTP.Status = 200 Then
                strFilePath = objFSO.BuildPath(strCurrentDir, strFile)
                Set objFile = objFSO.OpenTextFile(strFilePath, 2, True)
                objFile.Write objHTTP.responseText
                objFile.Close
            End If
        Next
        
        ' Update resources
        objHTTP.Open "GET", strGitHubRaw & "resources/qr.png", False
        objHTTP.send
        If objHTTP.Status = 200 Then
            strQRPath = objFSO.BuildPath(strResourcesDir, "qr.png")
            Set objStream = CreateObject("ADODB.Stream")
            objStream.Type = 1 ' Binary
            objStream.Open
            objStream.Write objHTTP.responseBody
            objStream.SaveToFile strQRPath, 2 ' Overwrite
            objStream.Close
        End If
        
        ' Save new hash
        Set objFile = objFSO.OpenTextFile(strHashFile, 2, True)
        objFile.Write strRemoteHash
        objFile.Close
        
        objShell.Popup "Update complete!", 2, "Bible Verse Finder Update", 64
    End If
End If
On Error Goto 0

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
    ' Only write to log if we want to track successful launches
    ' LogError "Application launched successfully"
End If
