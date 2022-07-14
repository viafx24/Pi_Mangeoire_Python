#! /usr/bin/python3

import time
import serial
import os


ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2)
ser.flushInput()


for i in range(100):
  time.sleep(0.05)
  if i % 2 ==0:
      print("I send 1")
      ser.write(b"1")
  else:
      print("I send 0")
      ser.write(b"0")
      
  #ser.write(b"1")
  #time.sleep(0.5)
  time.sleep(0.2)
  ser_bytes=ser.readline()
  Bytes_2_String=str(ser_bytes) 
  Pretty_Line=Bytes_2_String[2:len(Bytes_2_String)-5]
  print(Pretty_Line)
  
  
ser.close() # close serial port to allow uploading sketches
print("The Serial Port is closed")   

