import serial
import sys
import os
from datetime import datetime
import time
from subprocess import call
import pygame
from pygame.locals import *
import pygame.camera

call(["sudo", "/opt/vc/bin/tvservice", "-o"]) # stop hdmi

delay_between_iteration=0.1# le delai est en fait bien plus long
delay_pause=180


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

#remove all photos in the directory before beginning
#maybe not a good idea.

for f in os.listdir(Photo_Directory):
    os.remove(os.path.join(Photo_Directory, f))



#ser=serial.Serial('/dev/ttyUSB0',115200, timeout=2)
ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2)
#ser=serial.Serial('/dev/ttyS0',9600, timeout=2)
ser.flushInput()


time.sleep(1) # test 10 seconds in case of problem
 
Global_Iteration=0;
Number_Of_Pictures=0

Initial_T = datetime.now() 

while Number_Of_Pictures < 5000:
    
#         t = datetime.now() 
#         if (t.minute % 10 == 0) : # pause de 60 seconde toutes les 10 minutes de l'heure précise
#             print("Pause commence pour 60 secondes")
#             time.sleep(delay_pause)
#             print("Fin de la pause")    
        
        Send_String = ''
        
        while Send_String.count(',')!= 10:
                b=ser.readline()
                try:
                    Send_String = b.decode()
                except:
                        pass
        
 
            
                    
        
        floats = [float(x) for x in Send_String.split(",")]
        
            
        Boot_Count=floats[0]
        Raspi_Voltage=floats[1]
        Raspi_Current=floats[2]
        Solar_Voltage=floats[3]     
        Solar_Current=floats[4]
        LDR=floats[5]
        X=floats[6]
        Y=floats[7]
        Z=floats[8]
        PIR_Status=floats[9]
        PIR_Count=floats[10]
        
        #en python, le caractère d'échappement pour descendre sur la ligne d'en dessous est "\"
        Send_String= str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ',' + \
                     str(round(datetime.now().timestamp()-Initial_T.timestamp(),2)) + ','\
                     + str(Number_Of_Pictures) + ',' + str(Global_Iteration) + ','\
                     + Send_String 
        
        
        print(Send_String)
        
        with open("/home/pi/Documents/Python/Pi_Mangeoire_Python/Data_Ina219.txt","a")  as Data:
             Data.write(Send_String)

        if Solar_Voltage < (13.5 + 0.1) or LDR > (2000-200) :
            print("shutdown the pi in 10 sec")
            time.sleep(10)
            print("shutdown the pi")
            call("sudo nohup shutdown -h now", shell=True)
#
        
        if PIR_Status == 1:
            
            
                t = time.time()
                cam.start()
                #time.sleep(2)
                for iteration_Useless in range(3):#increase if firsts images not good
                    image = cam.get_image()
                for iteration in range(10):
                    Global_Iteration=Global_Iteration + 1
                    image = cam.get_image()
                    Name= "/home/pi/Documents/Pictures/USB_Cam_Mangeoire/picture_" + str(Global_Iteration)+ ".jpg" 		
                    pygame.image.save(image, Name)
                    print("photo number " + str(Global_Iteration )+ " saved")
                cam.stop()    
                print("Time to takes picture:" + str(time.time()-t))      
        
        #cam.stop()
            
        ser.flushInput()
        time.sleep(delay_between_iteration)
        Number_Of_Pictures=len(os.listdir('/home/pi/Documents/Pictures/USB_Cam_Mangeoire'))
#sys.exit()
#cam.stop()
print("Limite du nombre d'images atteinte.Fin du script.")            



