#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError

import time
import sys
import os

NUMBER_HOURS=30;
SAMPLE_PER_SECONDS=1
NUMBER_OF_INA=2
SHUNT_OHMS = 0.1

ina1 = INA219(SHUNT_OHMS)
ina1.configure()

if NUMBER_OF_INA == 2 :
    ina2 = INA219(SHUNT_OHMS,address=0x41)
    ina2.configure()

if os.path.isfile('/home/pi/Documents/Ina219/Data_Ina219.txt'):
    os.remove("/home/pi/Documents/Ina219/Data_Ina219.txt")


def read_loop():
    
    for i in range(1,int(NUMBER_HOURS*3600*SAMPLE_PER_SECONDS)):
        
        if NUMBER_OF_INA == 1 :
            Voltage=str(round(ina1.voltage(),2))
            Current=str(round(ina1.current(),2))
            DataIna= Voltage + "," + Current + "\n"
        
            print("Bus Voltage: %s V"  % Voltage)
            print("Bus Current: %s mA" % Current)
            
            
        if NUMBER_OF_INA == 2 :
            
            Voltage1=str(round(ina1.voltage(),2))
            Current1=str(round(ina1.current(),2))
            Voltage2=str(round(ina2.voltage(),2))
            Current2=str(round(ina2.current(),2))
            
            DataIna= Voltage1 + "," + Current1 + "," + Voltage2 + "," + Current2 +"\n"
            
            print("Bus Voltage: %s V"  % Voltage1)
            print("Bus Current: %s mA" % Current1)
            print("Bus Voltage: %s V"  % Voltage2)
            print("Bus Current: %s mA" % Current2)
                      
            
        Data=open("/home/pi/Documents/Ina219/Data_Ina219.txt","a")
        
        try:
            Data.write(DataIna)
        finally:
            Data.close()
        
       
        time.sleep(1/SAMPLE_PER_SECONDS)
        print("iteration:" + str(i))

t = time.time() 
read_loop()
print(time.time()-t)

sys.exit()



