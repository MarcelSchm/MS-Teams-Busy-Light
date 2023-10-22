import serial
import time

COM_PORT = "COM4"
COM_BAUD = 9600

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



