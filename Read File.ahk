#Requires AutoHotkey v2.0

#SingleInstance Force
;#include tf.ahk ; uncomment this line if you haven't included it your LIBrary
LogFilePath := "C:\Users\marcel.schmid\AppData\Roaming\Microsoft\Teams\logs.txt"
StatusArray := [] ;

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

MsgBox " Last Status: " StatusArray[StatusArray.Length]