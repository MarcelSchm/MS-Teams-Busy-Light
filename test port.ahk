#Requires AutoHotkey v2.0

#SingleInstance Force
PuttyPath := "C:\ErfinderTools\winPenPack\Bin\PuTTYPortable\PuTTYPortable.exe" 
If not FileExist(PuttyPath) 
{
	MsgBox PuttyPath " not found. "
	ExitApp
}

Run PuttyPath " -serial com15" ,,, &pid
WinWaitActive "ahk_pid " pid
sleep 9000
SendText "Red"
Winkill "PuTTY"
