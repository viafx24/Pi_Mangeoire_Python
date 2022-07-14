#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError

import time
import sys
import os


if os.path.isfile('/home/pi/Documents/Ina219/Data_Ina219.txt'):
    os.remove("/home/pi/Documents/Ina219/Data_Ina219.txt")


SHUNT_OHMS = 0.1


def read_loop(Number_Hours,SPS):
    
    for i in range(1,int(Number_Hours*3600*SPS)):
        
        String= str(round(ina.voltage(),2)) + "," + str(round(ina.current(),2)) + "\n"
        Data=open("/home/pi/Documents/Ina219/Data_Ina219.txt","a")
        try:
            Data.write(String)
        finally:
            Data.close()
            
        time.sleep(1/SPS)
        print(i)


ina = INA219(SHUNT_OHMS)
ina.configure()



print(sys.argv[1])
print(sys.argv[2])

t = time.time() 
read_loop(float(sys.argv[1]),float(sys.argv[2]))
print(time.time()-t)

sys.exit()



