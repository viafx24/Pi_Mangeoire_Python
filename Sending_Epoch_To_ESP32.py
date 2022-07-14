#! /usr/bin/python3

import time
import serial
import os
import datetime  


ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2)
ser.flushInput()

epoch_time = str(round(time.time()))


Date_Build=datetime.date.today() + datetime.timedelta(days=1)
Hour_Build=datetime.time(10,0, 0)
Wanted_Datetime = datetime.datetime(year = Date_Build.year, month = Date_Build.month,  day= Date_Build.day, hour = Hour_Build.hour,  minute= Hour_Build.minute, second = Hour_Build.second)
print(Wanted_Datetime )
epoch_next_time = round(Wanted_Datetime.timestamp())

Two_Epoch=epoch_time + ',' + str(epoch_next_time ) + ','

print(Two_Epoch)


ser.write(Two_Epoch.encode())
time.sleep(1)
#ser.write("256".encode())

#for i in range(20):
while 1:
#    epoch_time = str(round(time.time()))
#    print(epoch_time)
#    print(epoch_time.encode())
#    ser.write(epoch_time.encode())
#    ser.write(b"test")
    
#    time.sleep(0.1)
#    ser.flush()
#     ser.flushInput()
#    time.sleep(1)
    
#    print("first")
#     
    #ser_bytes=ser.readline().decode()
    #Pretty_Line=ser_bytes.decode()
    #print(Pretty_Line)
    if ser.in_waiting:
        print(ser.readline().decode())
#    print(ser.readline())
#    Bytes_2_String=str(ser_bytes) 
#   Pretty_Line=Bytes_2_String[2:len(Bytes_2_String)-5]
    

ser.close() # close serial port to allow uploading sketches
print("The Serial Port is closed")  

# for i in range(20):
#   time.sleep(0.5)
#   if i % 2 ==0:
#       print("I send 1")
#       ser.write(b"1")
#   else:
#       print("I send 0")
#       ser.write(b"0")
#       
#   
#   ser_bytes=ser.readline()
#   Bytes_2_String=str(ser_bytes) 
#   Pretty_Line=Bytes_2_String[2:len(Bytes_2_String)-5]
#   print(Pretty_Line)
#   
  
 

