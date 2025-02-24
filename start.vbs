Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objHTTP = CreateObject("MSXML2.XMLHTTP")

' Get current directory
strCurrentDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
objShell.CurrentDirectory = strCurrentDir

' GitHub API URL for the repository
strGitHubAPI = "https://api.github.com/repos/kinglunalilo/BibleVerseFinder/commits/main"
strGitHubRaw = "https://raw.githubusercontent.com/kinglunalilo/BibleVerseFinder/main/"

' File to store last commit hash
strHashFile = "last_commit.txt"
strLocalHash = ""

' Read stored hash if exists
If objFSO.FileExists(strHashFile) Then
    Set objFile = objFSO.OpenTextFile(strHashFile, 1)
    strLocalHash = objFile.ReadLine()
    objFile.Close()
End If

' Check for updates
objHTTP.Open "GET", strGitHubAPI, False
objHTTP.setRequestHeader "User-Agent", "BibleVerseFinder-UpdateChecker"
objHTTP.send

If objHTTP.Status = 200 Then
    ' Parse JSON response (simple string search since we only need the SHA)
    strResponse = objHTTP.responseText
    intStart = InStr(strResponse, """sha"":""") + 8
    intEnd = InStr(intStart, strResponse, """") - 1
    strRemoteHash = Mid(strResponse, intStart, intEnd - intStart + 1)
    
    ' Compare hashes
    If strLocalHash <> strRemoteHash Then
        ' Show update message
        objShell.Popup "Updates found! Downloading latest version...", 2, "Bible Verse Finder Update", 64
        
        ' List of files to update
        arrFiles = Array("search_scraper.py", "README.md", "LICENSE")
        
        ' Download each file
        For Each strFile In arrFiles
            objHTTP.Open "GET", strGitHubRaw & strFile, False
            objHTTP.send
            
            If objHTTP.Status = 200 Then
                Set objFile = objFSO.OpenTextFile(strFile, 2, True)
                objFile.Write objHTTP.responseText
                objFile.Close
            End If
        Next
        
        ' Save new hash
        Set objFile = objFSO.OpenTextFile(strHashFile, 2, True)
        objFile.Write strRemoteHash
        objFile.Close
        
        objShell.Popup "Update complete!", 2, "Bible Verse Finder Update", 64
    End If
End If

' Start the program
objShell.Run "pythonw search_scraper.py", 0, False
