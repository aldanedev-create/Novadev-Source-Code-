Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
homeDir = fso.GetParentFolderName(scriptDir)
logDir = homeDir & "\logs"
logPath = logDir & "\manager.log"

If Not fso.FolderExists(logDir) Then
  On Error Resume Next
  fso.CreateFolder(logDir)
  On Error GoTo 0
End If

command = """" & scriptDir & "\novadev-manager.cmd" & """"
exitCode = shell.Run(command, 0, True)

If exitCode <> 0 Then
  MsgBox "NovaDev Manager could not start." & vbCrLf & vbCrLf & _
         "Open this log for details:" & vbCrLf & logPath & vbCrLf & vbCrLf & _
         "Most common fix: install Python 3 from python.org with Tcl/Tk enabled.", _
         vbCritical, "NovaDev Manager"
End If
