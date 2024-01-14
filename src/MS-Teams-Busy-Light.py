import serial
import regex
from file_read_backwards import FileReadBackwards
from os import path
from easygui import *
import time
import sys
from datetime import datetime,timezone
import serial.tools.list_ports


COM_BAUD = 9600

def readCOMPorts():
   ports = serial.tools.list_ports.comports()
   if (len(ports) == 0):
      return 0 
   else:
      for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
      return sorted(ports)

def SelectCOMPorts():
   ports = readCOMPorts()
   msg ="Which COM-Port is your device connected to? Please Select from the List Below"
   title = "MS-Teams-Busy-Light"
   choices = []
   if (ports == 0):
      msg = "Unfortunately you have no COM-Port available in your System. Please check connections and start again."
      test = msgbox(msg,title,ok_button="Stop Program")
      sys.exit(0)
   for port, desc, hwid in ports:
      choices.append(port + ":  " + desc)
   if (len(choices) == 1):
      msg = "There is only 1 COM-Port available. Auto - Selected: \n\n" + choices[0]
      result = msgbox(msg,title,ok_button="OK")
      if (result == None):
         sys.exit(0) 
      else:    
         return port  
   choice = choicebox(msg, title, choices)  
   if (choice == None):
         sys.exit(0) 
   else:      
         return str.split(choice, ':')[0] 

def main():
   COM_PORT = SelectCOMPorts()
   ser = serial.Serial()
   ser.port = COM_PORT
   ser.baudrate = COM_BAUD
   LogFilePath = path.expandvars(r'%APPDATA%\Microsoft\Teams\logs.txt') 
   # Define the regex pattern
   regexPatternStatus = "(?=StatusIndicatorStateService: Added )(?!.*StatusIndicatorStateService:Added )[^\\(]+"
   regexPatternCalls = "DeviceCallControlManager Desktop: reportIncomingCall"
   status = 'initialize'
   now_script = datetime.now(timezone.utc) #timestamp from start to compare with last status in log file

   ser.open()
   time.sleep(3)
   ser.write(b'White')
         
   while 1:
      try:
         with FileReadBackwards(LogFilePath, encoding="utf-8") as frb:
            for l in frb:
               if not None == regex.search(regexPatternStatus,l):
                  now_statuslog = datetime.strptime("".join(l.split()[:6]), '%a%b%d%Y%H:%M:%SGMT%z') #Grab whole log string and extract timestamp
                  if now_script < now_statuslog:
                     status= l.split("Added ")[1].split(' ')[0]
                  else: 
                     status = "Outdated"
                  #msgbox(status) 
                  break
               if not None == regex.search(regexPatternCalls,l):
                  now_statuslog = datetime.strptime("".join(l.split()[:6]), '%a%b%d%Y%H:%M:%SGMT%z') #Grab whole log string and extract timestamp
                  if now_script < now_statuslog:
                     status= "IncomingCall"
                  else: 
                     status = "Outdated"       
                  
      except FileNotFoundError:
         msgbox(msg="can't open file: \n" + LogFilePath + "\n No such file or directory",title="FileNotFoundError in MS-Teams-Busy-Light Script") 

      match status:
         case "Available":
            ser.write(b'Green')
            time.sleep(2)
         case "Busy":
            ser.write(b'Red')
            time.sleep(2)
         case "InAMeeting":
            ser.write(b'Red')
            time.sleep(2)
         case "OnThePhone":
            ser.write(b'Red')
            time.sleep(2)
         case "DoNotDisturb":
            ser.write(b'Red')
            time.sleep(2)
         case "BeRightBack":
            ser.write(b'Yellow')
            time.sleep(2)
         case "Presenting":
            ser.write(b'Red')
            time.sleep(2)
         case "Away":
            ser.write(b'Yellow')
            time.sleep(2)
         case "Offline":
            ser.write(b'Yellow')
            time.sleep(2)
         case "Unknown":
            ser.write(b'Red')
            time.sleep(2)
         case "NewActivity":
            #ser.write(b'Red')
            time.sleep(2)
         case "ConnectionError":
            ser.write(b'Red')
            time.sleep(2)
         case "NoNetwork":
            ser.write(b'Red')
            time.sleep(2)
         case "Initialize":
            ser.write(b'White')
            time.sleep(2)
         case "Outdated":
            ser.write(b'Green')
            time.sleep(2)
         case "IncomingCall":
            ser.write(b'BlinkRed')
            time.sleep(2)
         case _:
            msgbox(msg="MS Teams Presence Status Script: The following Status is not yet known and needs to be added to the python Script: \n" + status,title="MS-Teams-Busy-Light Script")  
      time.sleep(2)      
            
   ser.close()

if __name__ == "__main__":
    sys.exit(main())