#! /usr/bin/python3

import time
import serial
import os

try :
    os.remove("/home/pi/Documents/Test_Chargeur_Lion/data_chargeur_Lion.txt")
    print("File Removed!")
    
except:
    
    print("File doesn't exist")

Max_File_Size = 8000000;



ser=serial.Serial('/dev/ttyUSB0',115200, timeout=20)
ser.flushInput()

time.sleep(2)


while True :
    try:
        ser_bytes=ser.readline()
    #    print(ser_bytes)
        Bytes_2_String=str(ser_bytes) 
        Pretty_Line=Bytes_2_String[2:len(Bytes_2_String)-5]
        
        print(Pretty_Line)
        
        with open("/home/pi/Documents/Test_Chargeur_Lion/data_chargeur_Lion.txt","a+") as Data:
            Data.write(Pretty_Line + "\n" )
            
        if os.stat("/home/pi/Documents/Test_Chargeur_Lion/data_chargeur_Lion.txt").st_size > Max_File_Size :
             break

    except KeyboardInterrupt:

        break    
                
            
ser.close() # close serial port to allow uploading sketches
print("The Serial Port is closed") 