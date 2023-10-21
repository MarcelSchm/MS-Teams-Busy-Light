#Requires AutoHotkey v2.0

#SingleInstance Force
;#include tf.ahk ; uncomment this line if you haven't included it your LIBrary
LogFilePath := A_AppData "\Microsoft\Teams\logs.txt"
StatusArray := [] ;

Loop {
LogFile := FileOpen(LogFilePath, "r")
; MsgBox LogFile.ReadLine()

; Define the regex pattern
regexPattern := "(?=StatusIndicatorStateService: Added )(?!.*StatusIndicatorStateService:Added )[^\\(]+"

; Loop through the lines in the file
While !LogFile.AtEOF
{
    line := LogFile.ReadLine()
    
    ; Check if the line matches the regex pattern
    if (RegExMatch(line, regexPattern))
    {
        ; Do something with the line that contains "StatusIndicatorStateService"
        match := RegExMatch(line, "\bAdded\s+\K\S+",&outputstatus) ; First pattern to get complete line, second pattern to get the actual status only
		;MsgBox "Found a line: " line ; only needed for debug purposes of regexPattern
		;MsgBox "actual Status: " outputstatus[]
		StatusArray.Push(outputstatus[])
    }
}

; Close the file
LogFile.Close()

;MsgBox " Last Status: " StatusArray[StatusArray.Length]
switch StatusArray[StatusArray.Length]
    {
	case "Available":
		;MsgBox "Available was read successfully"
	case "Busy":
		;MsgBox "Busy was read successfully"
	case "InAMeeting":
		;MsgBox "InAMeeting was read successfully"
	case "OnThePhone":
		;MsgBox "OnThePhone was read successfully"
	case "DoNotDisturb":
		;MsgBox "DoNotDisturb was read successfully"
	case "BeRightBack":
		;MsgBox "BeRightBack was read successfully"
	case "Presenting":
		;MsgBox "Presenting was read successfully"
	case "Away":
		;MsgBox "Away was read successfully"
	case "Offline":
		;MsgBox "Offline was read successfully"
	case "Unknown":
		;MsgBox "Unknown was read successfully"
	case "NewActivity":
		;MsgBox "NewActivity was read successfully"
	case "ConnectionError":
		;MsgBox "ConnectionError was read successfully"
	case "NoNetwork":
		;MsgBox "NoNetwork was read successfully"
	default:  ; Not Listed Status yet
		MsgBox "AutoHotkey Teams Presence Status Script: The following Status is not yet known and needs to be added to the autohotkey Script: " StatusArray[StatusArray.Length]
    }
Sleep 10000	
}