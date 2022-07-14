import time
import serial
import os
import datetime  


ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2)
ser.flushInput()

for i in range(20):
    
        if ser.in_waiting:
            print(ser.readline().decode())
            ser.write(b"test test test")
        time.sleep(1)