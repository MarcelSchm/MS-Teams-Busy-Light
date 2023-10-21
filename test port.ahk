#Requires AutoHotkey v2.0

#SingleInstance Force
DetectHiddenWindows true
if not A_IsAdmin
{
  Run '*RunAs "' A_ScriptFullPath '" /restart'
  Exit
}
PlinkPath := A_WorkingDir "\plink.exe" ; if you change location of plink, put path here
COMPORT := " -serial COM4" ;change COMPORT of Arduino here
CMDWinName := "cmd.exe" ; Name of cmd.exe in WIN11. Might Need to be changed depending on OS"WindowsTerminal.exe" 

If not FileExist(PlinkPath) 
{
	MsgBox PlinkPath " not found. "
	ExitApp
}

sleep 1000
Run "cmd  plink" COMPORT  , A_WorkingDir,"Hide", &PID
;Run cmd.exe  A_WorkingDir PlinkPath  COMPORT ;,,, &PID ;,,"Max",&PID
;WinWait "ahk_pid " ;PID 
WinWait "ahk_pid " PID  ; Wartet, bis es erscheint.
ControlSendText "plink" COMPORT "`n",,"cmd"
;ControlSendText "plink" COMPORT  ; Sendet Tasten direkt an die Eingabeaufforderung.
sleep 2001
ControlSendText "Red" "`n",, "cmd"
;ControlSendText "{Enter}",, "cmd"
Sleep 300
try 
	WinKill "cmd"
Catch as e 
	MsgBox(Type(e) " in " e.What ", das auf Zeile " e.Line " aufgerufen wurde.")