import serial
import time
import sys
from easygui import *
from serial.tools import list_ports

COM_PORT = "COM"
COM_BAUD = 9600

msg ="Which COM-Port is your device connected to? Please enter ONLY the Port number (so '4' for COM4)"
title = "MS-Teams-Busy-Light"
reply = enterbox(msg,title)
if reply :
    COM_PORT = COM_PORT + reply
else:
    #msgbox('You canceled the dialog.')
    sys.exit()

# COM_Port_List = list()
# for description in list_ports.comports():
#     COM_Port_List.append(description)
# if len(COM_Port_List) ==1:
#     COM_PORT = COM_Port_List[0].name
# else:
# choices = COM_Port_List  # Outputs list of available serial ports
# choice = choicebox(msg, title, choices)



ser = serial.Serial()
ser.port = COM_PORT
ser.baudrate = COM_BAUD

ser.open()
time.sleep(3)

ser.write(b'Red')
time.sleep(2)
ser.write(b'Green')
time.sleep(2)
ser.close()



