import glob
import serial, sys, os, time
import datetime
from subprocess import Popen, PIPE, STDOUT, DEVNULL, call, run
import smtplib
from math import nan



def main():
    
    print("ARE YOU SURE RELATIVE AND ABSOLUTE TIME ARE CORRECTLY SET ?")
    time.sleep(1)
    
    call(["sudo", "/opt/vc/bin/tvservice", "-o"]) # stop hdmi
    Open_Shared_Folder()
    Authorize_To_Write_Files()
    # Variables
    
    ABSOLUTE_STOP = True
    ABSOLUTE_START = True
    
    ## FOR BOTH
    
    day_to_stop = 0
    hour_to_stop = 23
    minute_to_stop = 59
    

    day_to_restart = 1
    hour_to_restart = 7
    minute_to_restart = 0
    


    epoch_to_stop=Compute_Hour_To_Stop(hour_to_stop,minute_to_stop,day_to_stop,ABSOLUTE_STOP)
    epoch_to_restart=Compute_Hour_To_Restart(hour_to_restart,minute_to_restart,day_to_restart,ABSOLUTE_START)
    

    Voltage_Limit_To_Shutdown_Raspi = 14.25

    Number_Of_Videos = 0
    Duration_of_Video = 60
    Frame_Per_Second = 10
    #resolution='1920x1080'
    #resolution='640x480'
    #resolution='1600x896'
    resolution='1024x768'
    Bitrate = '2M'
    Global_Iteration = 0
    
    
    ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2)
    ser.flushInput()
    
    Initial_T = datetime.datetime.now()
    
    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
        Data.write("Program launch at " + str(Initial_T) + "\n" )
            
            
    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Data_Raspi_Session.txt'):
        os.remove("//home/pi/mnt/USB_Cam_Mangeoire/Data_Raspi_Session.txt")        
    
    
    while Number_Of_Videos < 5000:
        
        Global_Iteration = Global_Iteration + 1
        
        time.sleep(0.1)
        Number_Of_Videos=len(os.listdir("//home/pi/mnt/USB_Cam_Mangeoire/Video"))
        time.sleep(0.1)
        
        Send_String=""
        
        
            #Send_String=ser.readline().decode()
       
        while 1:

           if ser.in_waiting:
               try:
                   Send_String=ser.readline().decode()
                   Send_String = Send_String.replace('\0', '')
                   
               except:
                   print("Continue of ser.readline() triggered")
                   print(Send_String)
                   with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                       Data.write("Continue of ser.readline() triggered" + "\n" )
                       Data.write(Send_String + "\n")
                       
                   Global_Iteration = Global_Iteration - 1
                   continue
               break
 

        
        try:
                        
            floats = [float(x) for x in Send_String.split(",")]

                      
                        
        except:
                      
            print("Continue of float triggered")
            print(Send_String)
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                Data.write("Continue of float triggered" + "\n" )
                Data.write(Send_String + "\n")
                
            Global_Iteration = Global_Iteration - 1
            continue    

        

        if len(floats) < 7 : #sometimes error due to floats size inf to 3
    
            print(len(floats))
          
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                  
                Data.write("Continue of LENGTH float triggered" + "\n" )
                Data.write(Send_String + "\n")
                Data.write("Lenght float: "+ str(len(floats)) + "\n")
            
            Global_Iteration = Global_Iteration - 1
                  
            continue
                
        Transistor_State=floats[0]
        Reboot_Reason=floats[1]
        Raspi_Voltage=floats[2]
        Raspi_Current=floats[3]   
        Solar_Current=floats[4]
        Current_Epoch=floats[5]
        Epoch_Start=floats[6]
        
        if Epoch_Start == 1600000000 and Global_Iteration == 1:
            
            if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt'):
                os.remove("//home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt") 
            
        
        if Transistor_State == 0 and Reboot_Reason > 0:
            Received_All_Transistor_Off_Data_from_ESP32(ser)
            
            print("Continue of Transistor_OFF_Transfert triggered")
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                Data.write("Continue of Transistor_OFF_Transfert triggered" + "\n" )
                
            ser.flushInput()
            
            continue
        
              
        Send_String= str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ',' + \
                     str(round(datetime.datetime.now().timestamp()-Initial_T.timestamp(),2)) + ','\
                     + str(Number_Of_Videos) + ',' + str(Global_Iteration) + ','\
                     + Send_String 
        
        print(Send_String)
        
        with open("//home/pi/mnt/USB_Cam_Mangeoire/Data_All.txt","a")  as Data:
             Data.write(Send_String)
        
        with open("//home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt","a")  as Data:
             Data.write(Send_String)
             
             
        with open("//home/pi/mnt/USB_Cam_Mangeoire/Data_Raspi_Session.txt","a")  as Data:
             Data.write(Send_String)
        

        if Raspi_Voltage < (Voltage_Limit_To_Shutdown_Raspi) :            
            
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                 Data.write("Entering the close condition due to Voltage limit measured at " + str(Raspi_Voltage) + " at "  + str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))+ "\n" )
            
            #Send_Epoch_To_Esp32(ser,epoch_to_restart)
            Send_Voltage_Break_To_Esp32(ser)
            
            print("shutdown the pi in 10 sec")
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                 Data.write("shutdown the pi in 10 sec" + "\n" )
                 
            time.sleep(10)
            print("shutdown the pi")
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                 Data.write("shutdown the pi" + "\n" + "\n" )
                 
            run("sudo pkill -1 python3 ; sleep 10 ; sudo shutdown -h now", shell=True) # shutdown doesn't work without this command. dont know why.
            time.sleep(20)
        
        elif round(time.time()) > epoch_to_stop:
            
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                 Data.write("Entering the close condition due to Time limit  at " + str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " at voltage "+ str(Raspi_Voltage) + "\n" )
            
            Send_Epoch_To_Esp32(ser,epoch_to_restart)
            
            print("shutdown the pi in 10 sec")
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                 Data.write("shutdown the pi in 10 sec" + "\n" )
                 
            time.sleep(10)
            print("shutdown the pi")
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                 Data.write("shutdown the pi" + "\n" + "\n")
            
            run("sudo pkill -1 python3 ; sleep 10 ; sudo shutdown -h now", shell=True) # shutdown doesn't work without this command. dont know why.
            time.sleep(20)
                                        
        Iteration_Of_Video=Get_Iteration_Of_Video() #based on iteration of the last modified file
        Lead_Zero_Iteration=str(Iteration_Of_Video).zfill(5)
        video_name= "//home/pi/mnt/USB_Cam_Mangeoire/Video/video_" + Lead_Zero_Iteration + ".mp4" 

        # compression operates in the background. Change Popen by run if want not in the background
        
        ser.flushInput() # pour eviter d'avoir le buffer qui se remplit si l'esp32 produit des lignes à une vitesse
        #superieur . a noter que le temps noté alors est susceptible d'être inexact à une minute prés (si le pas est 1
        #minute)
        
        t = time.time()
        print("Acquiring video...")
        
        run([
        'ffmpeg',
        '-f', 'alsa',     #for sound
        '-channels', '1',
        '-i', 'plughw:3,0', #for sound
        '-f', 'v4l2', #for video input
        '-s', resolution, 
        '-i', '/dev/video2', #the video input (USB cam
        '-t', str(Duration_of_Video), # time in second of video
        '-r', str(Frame_Per_Second), # framerate (5 would be 5fps )
        '-c:v', 'h264_omx', #raspi efficient hardware codec
        '-b:v', Bitrate, # level of compression 4M tp 16M should give similar result. less would decrease quality
        '-acodec', 'aac', #audio codec MP3 for efficient compression
        video_name,
        '-y', #erase the file if aleady exist
        ],
#        stdout=DEVNULL,# removing output in the terminal: comment if bug to see stdout
        stderr=STDOUT,
#        stderr=DEVNULL,    
        )
        
        print("Time to take video:" + str(time.time()-t))

        

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


def Compute_Hour_To_Restart(hour_to_restart,minute_to_restart,day_to_restart,ABSOLUTE_START):


    
        
    if ABSOLUTE_START == True :
        
        Date_Build=datetime.datetime.today()  + datetime.timedelta(days=day_to_restart)
        Wanted_Datetime = datetime.datetime(year = Date_Build.year, month = Date_Build.month,  day= Date_Build.day,\
        hour = hour_to_restart,  minute= minute_to_restart, second = 0)
           
        
    elif ABSOLUTE_START == False:
        
        Date_Build=datetime.datetime.today()  + datetime.timedelta(days=day_to_restart,hours=hour_to_restart,\
        minutes=minute_to_restart)
        Wanted_Datetime = datetime.datetime(year = Date_Build.year, month = Date_Build.month,  day= Date_Build.day,\
        hour = Date_Build.hour,  minute= Date_Build.minute, second = 0)
    
    
    epoch_to_restart= round(Wanted_Datetime.timestamp())
    print('Raspi will restart: ' + str(Wanted_Datetime) )
    
    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
        Data.write('Raspi will restart: ' + str(Wanted_Datetime) + "\n" )
    
    return epoch_to_restart
    
def Compute_Hour_To_Stop(hour_to_stop, minute_to_stop,day_to_stop,ABSOLUTE_STOP):
    

    
    if ABSOLUTE_STOP == True :
        
        Date_Build=datetime.datetime.today()  + datetime.timedelta(days=day_to_stop)
        Wanted_Datetime = datetime.datetime(year = Date_Build.year, month = Date_Build.month,\
        day= Date_Build.day, hour = hour_to_stop,  minute= minute_to_stop, second = 0)
        
    elif  ABSOLUTE_STOP == False :
        
        Date_Build=datetime.datetime.today()  + datetime.timedelta(days=day_to_stop,hours=hour_to_stop,\
        minutes=minute_to_stop)
        Wanted_Datetime = datetime.datetime(year = Date_Build.year, month = Date_Build.month,\
        day= Date_Build.day, hour = Date_Build.hour,  minute= Date_Build.minute , second = 0)
        
    epoch_to_stop = round(Wanted_Datetime.timestamp())
    
    print("Raspi will stop: "  + str(Wanted_Datetime) )
    
    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
        Data.write('Raspi will stop: ' + str(Wanted_Datetime) + "\n" )
    
    return epoch_to_stop


def Get_Iteration_Of_Video():


    list_of_files = glob.glob('//home/pi/mnt/USB_Cam_Mangeoire/Video/*') # * means all if need specific format then *.csv


    if  len(list_of_files) > 0    : 
        latest_file = max(list_of_files, key=os.path.getctime)
        Iteration_Of_Last_Video = int(latest_file[-9:-4])
        Iteration_Of_Video = Iteration_Of_Last_Video + 1
        print(Iteration_Of_Video)
          
    else :
        Iteration_Of_Video = 1
        print(Iteration_Of_Video)

    return Iteration_Of_Video


def Send_Epoch_To_Esp32(ser,epoch_to_restart):
    
    i = 0
    j = 0
    ser.reset_input_buffer()
    while 1:
        
        j=j+1
        if ser.in_waiting: #to avoid to do the ser.write during light sleep.
            i = i+1
            
            if i == 1:
                #print(i)
                Two_Epoch= "Epoch Sent," + str(round(time.time())) + ',' + str(epoch_to_restart ) + ','
                Line=ser.readline().decode()
                print(Line)
                with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                     Data.write(Line)
                     
                ser.write(Two_Epoch.encode())
                print(Two_Epoch)
                time.sleep(10) #critical

            if ser.in_waiting:
                Line=ser.readline().decode()
                print(Line)
                print(i)
                
                with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                    Data.write(Line)
                    Data.write(str(i) + "\n")
                
                if Line == "Epoch received\r\n":
                    break
                else:
                    
                    epoch_to_restart=epoch_to_restart + 300 # add 5 minutes (300 sec) if failed
                    print("problem:Epoch not received in second if")
                    print("New epoch_to_restart= " + str(epoch_to_restart))
                    
                    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                        Data.write("problem:Epoch not received in second if" + "\n" )
                        Data.write("New epoch_to_restart= " + str(epoch_to_restart) + "\n" )
                        
                    
                    i=0
             else:
                 
                 print("problem:Break not received in first if)
                            
                 with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                                Data.write("problem:Break not received in first if" + "\n" )                       
                            
                 i=0       
                    
                    
                        
        time.sleep(1)         



def Send_Voltage_Break_To_Esp32(ser):
    
    i = 0
    j = 0
    ser.reset_input_buffer()
    while 1:
        
        j=j+1
        if ser.in_waiting: #to avoid to do the ser.write during light sleep.
            i = i+1
            
            if i == 1:
                Line=ser.readline().decode()
                print(Line)
                with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                     Data.write(Line)

                ser.write("Break Sent,".encode())
                print("Break Sent")
                time.sleep(10) #critical

            if ser.in_waiting:
                Line=ser.readline().decode()
                print(Line)
                print(i)
                
                with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                    Data.write(Line)
                    Data.write(str(i) + "\n")
                
                if Line == "Break received\r\n":
                    break
                else:
                    
                    print("problem:Break not received in second if")
                    
                    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                        Data.write("problem:Break not received in second if" + "\n" )                       
                    
                    i=0
            else:
                 
                print("problem:Break not received in first if)
                        
                with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                            Data.write("problem:Break not received in first if" + "\n" )                       
                        
                i=0
                    
                    
                        
        time.sleep(1)



def Authorize_To_Write_Files():

# give right to write in ina tdg if already exist and created as sudo user in rc.local
# useful when call from thonny vs from rc.local I think. but i have doubt.

    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Data_All.txt'):

        call("sudo chmod 777 //home/pi/mnt/USB_Cam_Mangeoire/Data_All.txt", shell=True)

    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Log.txt'):
    
        call("sudo chmod 777 //home/pi/mnt/USB_Cam_Mangeoire/Log.txt", shell=True)
        
    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt'):
        
        call("sudo chmod 777 //home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt", shell=True)
        
        
    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Data_Raspi_Session.txt'):
        
        call("sudo chmod 777 //home/pi/mnt/USB_Cam_Mangeoire/Data_Raspi_Session.txt", shell=True)



def Received_All_Transistor_Off_Data_from_ESP32(ser):
        
    i = 0

    while 1:

        if ser.in_waiting:
            
            
            if i == 1:
                Line=ser.readline().decode()
                ser.write("Raspi Ready sent".encode())
                print("Raspi Ready sent")
                
                with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                        Data.write("Raspi Ready sent" + "\n" )
                
                time.sleep(2) # soudl be rather 10 ?
            
            
            i = i+1

            if i == 2:
                Line=ser.readline().decode()
                if Line == "ESP32 Ready received\r\n":
                    print("ESP32 Ready received")
                    
                    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                        Data.write("ESP32 Ready received" + "\n" )
                    
                    time.sleep(2)

            
            else:
                
                Send_String=ser.readline().decode()
                
                if Send_String == "End of transmission\r\n":
                    print("End of transmission")
                    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                        Data.write("End of transmission" + "\n" )
                    
                    break
                
                else:

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
                    
                        
                    with open("//home/pi/mnt/USB_Cam_Mangeoire/Data_All.txt","a")  as Data:
                        Data.write(Send_String)
        
                    with open("//home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt","a")  as Data:
                         Data.write(Send_String)
                        

                                   
               
        time.sleep(0.005)



if __name__ == '__main__':
    main()



  
#command='ffmpeg -f v4l2 -r 5 -s 1920x1080 -input_format yuyv422 -i /dev/video0 -t 100 -r 5 -c:v libx264 -crf 23 -preset ultrafast -vf format=yuv420p  /home/pi/mnt/USB_Cam_Mangeoire/out.mp4 -y'
#command='ffmpeg -f v4l2 -input_format mjpeg -r 5 -s 1920x1080 -input_format yuyv422 -i /dev/video0 -t 15 -r 1 -c:v h264_omx /home/pi/mnt/USB_Cam_Mangeoire/out.mp4 -y'
#command='ffmpeg -f v4l2  -input_format yuyv422  -r 5 -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 16M /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
#command='ffmpeg -f v4l2  -input_format mjpeg  -r 20 -s 1920x1080 -i /dev/video0 -t 30 -r 20 -c:v copy  /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
#command='ffmpeg  -i /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4  -c:v h264_omx  -b:v 16M  /home/pi/mnt/USB_Cam_Mangeoire/out_MJPEG_Then_OMX.mp4 -y'
#command='ffmpeg -ar 44100 -ac 1 -f alsa  -i plughw:2,0 -f v4l2  -input_format yuyv422  -r 5 -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 8M -acodec aac /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
#command='ffmpeg -f alsa  -i plughw:2,0 -f v4l2  -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 8M -acodec libmp3lame /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'

