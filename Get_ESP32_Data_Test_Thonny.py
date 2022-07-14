import serial
import sys
import os
from datetime import datetime
import time
from subprocess import call
import pygame
from pygame.locals import *
import pygame.camera
    

delay_between_iteration=1;


Photo_Directory="/home/pi/Documents/Pictures/USB_Cam_Mangeoire"
prefix = "Image_"

width=1920
height=1080

#initialise pygame
pygame.init()
pygame.camera.init()
#cam.stop()
cam = pygame.camera.Camera("/dev/video0",(width,height))



if os.path.isfile('/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt'):
    os.remove("/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt")

Photo_Directory="/home/pi/Documents/Pictures/USB_Cam_Mangeoire"
prefix = "Image_"
#ser=serial.Serial('/dev/ttyUSB0',115200, timeout=2)
ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2)
ser.flushInput()


time.sleep(1) # test 10 seconds in case of problem
 
Global_Iteration=0;
cam.start()
while Global_Iteration < 4000:
    
    try :
     #ser.flushInput()
        b=ser.readline()
        string_n = b.decode()
#    string = string_n.rstrip()    
     

    # now = datetime.now()  
    # Time= str(datetime.now())
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # Send_String= dt_string + "," + string_n
        Send_String= string_n
        print(Send_String)
        
        
        floats = [float(x) for x in string_n.split(",")]
        
            
        Boot_Count=floats[0]
        Raspi_Voltage=floats[1]
        Raspi_Current=floats[2]
        Solar_Voltage=floats[3]     
        Solar_Current=floats[4]
        PIR_Status=floats[5]
        with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt","a")  as Data:
             Data.write(Send_String)

        if Solar_Voltage < 14.82 :# or Solar_Current > 0 :
            print("shutdown the pi in 10 sec")
            time.sleep(10)
            print("shutdown the pi")
            call("sudo nohup shutdown -h now", shell=True)
#
        
        if PIR_Status == 1:
            
                t = time.time()

            
                for iteration in range(10):
                    Global_Iteration=Global_Iteration + 1
                    image = cam.get_image()
                    #time.sleep(5)
                    Name= "/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_" + str(Global_Iteration)+ ".jpg" 		
                    pygame.image.save(image, Name)
                    print("photo number " + str(Global_Iteration )+ " saved")
                #cam.stop()    
                print("Time to takes picture:" + str(time.time()-t))      
        
    except :        
        print("Probable float error conversion")
#            cam.stop()
            
    ser.flushInput()
    time.sleep(delay_between_iteration)
#sys.exit()
cam.stop()
            

# datetime object containing current date and time
#now = datetime.now()
 
# print("now =", now)

# # dd/mm/YY H:M:S
# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# print("date and time =", dt_string)	





# def read_loop():
    
#     for i in range(1,int(NUMBER_HOURS*3600*SAMPLE_PER_SECONDS)):
    
            
#             Voltage1=str(round(ina3221.getBusVoltage_V(RASPI_CHANNEL),2))
#             Current1=str(round(ina3221.getCurrent_mA(RASPI_CHANNEL),2))
#             Voltage2=str(round(ina3221.getBusVoltage_V(SOLAR_CELL_CHANNEL),2))
#             Current2=str(round(ina3221.getCurrent_mA(SOLAR_CELL_CHANNEL),2))
            
#             DataIna= Voltage1 + "," + Current1 + "," + Voltage2 + "," + Current2 +"\n"
            
#             print("Bus Voltage: %s V"  % Voltage1)
#             print("raspi Current: %s mA" % Current1)
#             print("Bus Voltage: %s V"  % Voltage2)
#             print("solar panel Current: %s mA" % Current2)
                      
            
#             Data=open("/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt","a")
        
#             try:
#                 Data.write(DataIna)
#             finally:
#                 Data.close()
        
       
#             time.sleep(1/SAMPLE_PER_SECONDS)
#             print("iteration:" + str(i))

# t = time.time() 
# read_loop()
# print(time.time()-t)

# sys.exit()

