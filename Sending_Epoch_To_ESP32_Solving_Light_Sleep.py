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

#epoch_next_time = int(epoch_time) + 7230

Two_Epoch=epoch_time + ',' + str(epoch_next_time ) + ','

print(Two_Epoch)


#ser.write(Two_Epoch.encode())
#time.sleep(0.05)
#ser.write("256".encode())

#for i in range(20):
#for i in range(50):
i=0
while 1:

    if ser.in_waiting:
        i=i+1
        print(ser.readline().decode())
        if i == 1:
            ser.write(Two_Epoch.encode())
        
    time.sleep(0.05)
#    ser.flush()

ser.close() # close serial port to allow uploading sketches
print("The Serial Port is closed")  

 

