#Requires AutoHotkey v2.0

#SingleInstance Force
DetectHiddenWindows true
if not A_IsAdmin
{
  Run '*RunAs "' A_ScriptFullPath '" /restart' ;Admin rights needed, so that ControlSendText will work in Hidden Mode.
  Exit
}

PlinkPath := A_WorkingDir "\plink.exe" ; if you change location of plink, put path here
COMPORT := " -serial COM4" ;change COMPORT of Arduino here

If not FileExist(PlinkPath) 
{
	MsgBox PlinkPath " not found. "
	ExitApp
}


Run "cmd  plink" COMPORT  , A_WorkingDir,"max", &PID
WinWait "ahk_pid " PID  ; Wartet, bis es erscheint.
ControlSendText "plink" COMPORT "`n",,"cmd"
Sleep 3001
Loop
{
	SetKeyDelay 30
	ControlSendText "Red `n" ,, "cmd"
	Sleep 5000
	ControlSendText "Green `n",, "cmd"
	Sleep 5000
}
try 
	WinKill "cmd"
Catch as e 
	MsgBox(Type(e) " in " e.What ", das auf Zeile " e.Line " aufgerufen wurde.")