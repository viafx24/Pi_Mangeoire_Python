#! /usr/bin/python3

import time
import serial

import os


os.remove("/home/pi/Documents/Test_Solar_Panel_Python/data_Solar_Panel.txt")
print("File Removed!")

ser=serial.Serial('/dev/ttyUSB0',115200, timeout=20)
ser.flushInput()

time.sleep(2)

ser.write(b"1") # can't send a string directlyt, need to convert in bytes thus add the little b, arduino then get a char.

time.sleep(2)

while True:
    ser_bytes=ser.readline()
#    print(ser_bytes)
    Bytes_2_String=str(ser_bytes) 
    Pretty_Line=Bytes_2_String[2:len(Bytes_2_String)-5]
    
    print(Pretty_Line)
    
    with open("/home/pi/Documents/Test_Solar_Panel_Python/data_Solar_Panel.txt","a+") as Data:
        Data.write(Pretty_Line + "\n" )
        
    if os.stat("/home/pi/Documents/Test_Solar_Panel_Python/data_Solar_Panel.txt").st_size > 6000:
        
        #ser_bytes=ser.readline()
        if Pretty_Line[0] != "K":
            #time.sleep(0.01)
            continue
        
  #      time.sleep(0.02)
  
        if Pretty_Line[0] == "K":
            
            ser_bytes=ser.readline()
            print(ser_bytes)
            Bytes_2_String=str(ser_bytes) 
            Pretty_Line=Bytes_2_String[2:len(Bytes_2_String)-5]
            
            print(Pretty_Line)
            while Pretty_Line != "Se":
                
                ser_bytes=ser.readline()
                print(ser_bytes)
                Bytes_2_String=str(ser_bytes) 
                Pretty_Line=Bytes_2_String[2:4]
                print(Pretty_Line)
                ser.write(b"0") # stop the motors
 #           time.sleep(0.02)
 #           ser.write(b"0") # stop the motors

            
            ser_bytes=ser.readline()
            print(ser_bytes)
       #    time.sleep(0.02)
            
       #     time.sleep(2)
            ser_bytes=ser.readline()
            print(ser_bytes)
            ser_bytes=ser.readline()
            print(ser_bytes)
            ser_bytes=ser.readline()
            print(ser_bytes)
            
            break


ser.close() # close serial port to allow uploading sketches
print("SerialPort close") 