import serial
import os
from datetime import datetime
import time

ser=serial.Serial('/dev/ttyUSB0',115200, timeout=2)
ser.flushInput()

if os.path.isfile('/home/pi/Documents/data_XYZ.txt'):
    os.remove("/home/pi/Documents/data_XYZ.txt")
#    print("Previous XYZ file Removed!")


time.sleep(10) # test 10 seconds in case of problem

for i in range(0,4000000):
    
    b=ser.readline()
    string_n = b.decode()
#    string = string_n.rstrip()    
    Data=open("/home/pi/Documents/data_XYZ.txt","a")    
    Time= str(datetime.now())
    Send_String=Time + "," + string_n
#    print(Send_String)
    Data.write(Send_String)
