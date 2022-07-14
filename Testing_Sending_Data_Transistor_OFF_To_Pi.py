import serial, sys, os, time
import smtplib
from subprocess import Popen, PIPE, STDOUT, DEVNULL, call, run
import datetime
from math import nan

def Open_Shared_Folder():
        
    process = Popen(
        "sudo mount -t cifs //192.168.1.1/CleMichel /home/pi/mnt -o vers=1.0,username=pi,password=cardyna!",
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
    )
    
    time.sleep(1)# to avoid a print blanck line
    while process.poll() is None:
        print(process.stdout.readline()) 


Open_Shared_Folder()
ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2)
ser.flushInput()
 

i = 0

while 1:

    if ser.in_waiting:
        
        
        if i == 1:
            Line=ser.readline().decode()
            ser.write("Raspi Ready sent".encode())
            print("Raspi Ready sent")
            time.sleep(10)
        
        
        i = i+1

        if i == 2:
            Line=ser.readline().decode()
            if Line == "ESP32 Ready received\r\n":
                print("ESP32 Ready received")
                time.sleep(2)
#         if i == 
#         elif Line == "End of transmission\r\n":
#             print("End of transmission")
#             break
        
        else:
            
            Send_String=ser.readline().decode()
            
            if Send_String == "End of transmission\r\n":
                print("End of transmission")
                break
            
            else:
#             Send_String = ''       
#             while Send_String.count(',')!= 6:
#                     b=ser.readline()
#                     try:
#                         Send_String = b.decode()
#                     except:
#                             pass


                try:
                    
                    floats = [float(x) for x in Send_String.split(",")]
                    
                except:
                    continue
                
                
                Transistor_State=floats[0]
                Reboot_Reason=floats[1]
                Raspi_Voltage=floats[2]
                Raspi_Current=floats[3]   
                Solar_Current=floats[4]
                Current_Epoch=floats[5]
                Epoch_Start=floats[6]
                
                Send_String= str(datetime.datetime.fromtimestamp(Current_Epoch).strftime("%d/%m/%Y %H:%M:%S")) + ',' + \
                str(float(nan)) + ','\
                + str(float(nan)) + ',' + str(float(nan)) + ','\
                + Send_String 
        
                print(Send_String)
                with open("//home/pi/mnt/USB_Cam_Mangeoire/Data_Ina219.txt","a")  as Data:
                    Data.write(Send_String)
                
            
           
    time.sleep(0.005)



