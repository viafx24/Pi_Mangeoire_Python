#! /usr/bin/python3

import time
import serial
import os

if os.path.exists("/home/pi/Documents/Test_Solar_Panel_Python/data_Solar_Panel.txt"):
    os.remove("/home/pi/Documents/Test_Solar_Panel_Python/data_Solar_Panel.txt")
Max_File_Size = 80000000;

print("File Removed!")

ser=serial.Serial('/dev/ttyUSB0',9600, timeout=20)
ser.flushInput()

time.sleep(2)

ser.write(b"1") # can't send a string directlyt, need to convert in bytes thus add the little b, arduino then get a char.

time.sleep(2)

while True:
    try:
        ser_bytes=ser.readline()
    #    print(ser_bytes)
        Bytes_2_String=str(ser_bytes) 
        Pretty_Line=Bytes_2_String[2:len(Bytes_2_String)-5]
        
        print(Pretty_Line)
        
        with open("/home/pi/Documents/Test_Solar_Panel_Python/data_Solar_Panel.txt","a+") as Data:
            Data.write(Pretty_Line + "\n" )
            
        if os.stat("/home/pi/Documents/Test_Solar_Panel_Python/data_Solar_Panel.txt").st_size > Max_File_Size:
            
            ser_bytes=ser.readline()
            Bytes_2_String=str(ser_bytes) 
            Pretty_Line=Bytes_2_String[2:len(Bytes_2_String)-5]
            
            print(Pretty_Line)
            while Pretty_Line != "Motors Stopped":
                print("Wait for stopping")
                ser_bytes=ser.readline()
                Bytes_2_String=str(ser_bytes) 
                Pretty_Line=Bytes_2_String[2:len(Bytes_2_String)-5]
                print(Pretty_Line)
                ser.write(b"0") # stop the motors
            
            break 


    except KeyboardInterrupt:
                    
        ser_bytes=ser.readline()
        Bytes_2_String=str(ser_bytes) 
        Pretty_Line=Bytes_2_String[2:len(Bytes_2_String)-5]
        
        print(Pretty_Line)
        while Pretty_Line != "Motors Stopped":
            print("Wait for stopping")
            ser_bytes=ser.readline()
            Bytes_2_String=str(ser_bytes) 
            Pretty_Line=Bytes_2_String[2:len(Bytes_2_String)-5]
            print(Pretty_Line)
            ser.write(b"0") # stop the motors
        
        break    
                
            
ser.close() # close serial port to allow uploading sketches
print("The Serial Port is closed") 