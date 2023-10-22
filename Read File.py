import regex
from file_read_backwards import FileReadBackwards
from os import path
from easygui import *
import time

LogFilePath = path.expandvars(r'%APPDATA%\Microsoft\Teams\logs.txt') 
# Define the regex pattern
regexPattern = "(?=StatusIndicatorStateService: Added )(?!.*StatusIndicatorStateService:Added )[^\\(]+"
status = ''
        
while 1:
   try:
      with FileReadBackwards(LogFilePath, encoding="utf-8") as frb:
         for l in frb:
            if not None == regex.search(regexPattern,l):
               status= l.split("Added ")[1].split(' ')[0]
               #msgbox(status) 
               break       
               
   except FileNotFoundError:
      msgbox(msg="can't open file: \n" + LogFilePath + "\n No such file or directory",title="FileNotFoundError") 

   match status:
      case "Available":
         msgbox("Available was read successfully")
      case "Busy":
         msgbox("Busy was read successfully")
      case "InAMeeting":
         msgbox("InAMeeting was read successfully")
      case "OnThePhone":
         msgbox("OnThePhone was read successfully")
      case "DoNotDisturb":
         msgbox("DoNotDisturb was read successfully")
      case "BeRightBack":
         msgbox("BeRightBack was read successfully")
      case "Presenting":
         msgbox("Presenting was read successfully")
      case "Away":
         msgbox("Away was read successfully")
      case "Offline":
         msgbox("Offline was read successfully")
      case "Unknown":
         msgbox("Unknown was read successfully")
      case "NewActivity":
         msgbox("NewActivity was read successfully")
      case "ConnectionError":
         msgbox("ConnectionError was read successfully")
      case "NoNetwork":
         msgbox("NoNetwork was read successfully")
      case _:
         msgbox("MS Teams Presence Status Script: The following Status is not yet known and needs to be added to the python Script: \n" + status)  
   time.sleep(10)      
         


