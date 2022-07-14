
#!/usr/bin/env python

import sys
import os
import time
import SDL_Pi_INA3221

NUMBER_HOURS=30;
SAMPLE_PER_SECONDS=1

RASPI_CHANNEL = 1
SOLAR_CELL_CHANNEL   =  3


if os.path.isfile('/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt'):
    os.remove("/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt")


ina3221 = SDL_Pi_INA3221.SDL_Pi_INA3221(addr=0x40)


def read_loop():
    
    for i in range(1,int(NUMBER_HOURS*3600*SAMPLE_PER_SECONDS)):
    
            
            Voltage1=str(round(ina3221.getBusVoltage_V(RASPI_CHANNEL),2))
            Current1=str(round(ina3221.getCurrent_mA(RASPI_CHANNEL),2))
            Voltage2=str(round(ina3221.getBusVoltage_V(SOLAR_CELL_CHANNEL),2))
            Current2=str(round(ina3221.getCurrent_mA(SOLAR_CELL_CHANNEL),2))
            
            DataIna= Voltage1 + "," + Current1 + "," + Voltage2 + "," + Current2 +"\n"
            
            print("Bus Voltage: %s V"  % Voltage1)
            print("raspi Current: %s mA" % Current1)
            print("Bus Voltage: %s V"  % Voltage2)
            print("solar panel Current: %s mA" % Current2)
                      
            
            Data=open("/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt","a")
        
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

