import glob
import serial, sys, os, time
import datetime
from subprocess import Popen, PIPE, STDOUT, DEVNULL, call, run
import smtplib
from math import nan



def main():
    
    print("ARE YOU SURE RELATIVE AND ABSOLUTE TIME ARE CORRECTLY SET ?")
    time.sleep(35) # let raspi config everything at boot (needed when launch from rc.local)
    
    call(["sudo", "/opt/vc/bin/tvservice", "-o"]) # stop hdmi
    Open_Shared_Folder()# to write video on the internet box
    Authorize_To_Write_Files()

    # Variables
    
    ABSOLUTE_STOP = True
    ABSOLUTE_START = True
     
    # ABSOLUTE_STOP = False
    # ABSOLUTE_START = False
    
    day_to_stop = 0
    hour_to_stop = 16
    minute_to_stop = 0
    
    day_to_restart = 1
    hour_to_restart = 5
    minute_to_restart = 30
    
    epoch_to_stop=Compute_Hour_To_Stop(hour_to_stop,minute_to_stop,day_to_stop,ABSOLUTE_STOP)
    epoch_to_restart=Compute_Hour_To_Restart(hour_to_restart,minute_to_restart,day_to_restart,ABSOLUTE_START)
    
    Voltage_Limit_To_Shutdown_Raspi = 14.25

    Number_Of_Videos = 0
    Duration_of_Video = 600
    Frame_Per_Second = 5
    # resolution='1920x1080'
    # resolution_2='1600x896'
    # resolution='640x480'
    # resolution='1024x768'
    resolution='1600x896'
    Bitrate = '2M'
# Bitrate_2 = '1M'
    Global_Iteration = 0
    
    
    ser=serial.Serial('/dev/ttyAMA0',9600, timeout=2) #serial communication with esp32
    ser.flushInput()
    
    Initial_T = datetime.datetime.now()
    
    with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
        Data.write("Program launch at " + str(Initial_T) + "\n" )
            
    # specific log file of a raspi session (remove it each time raspi boot)
            
    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Data_Raspi_Session.txt'):
        os.remove("//home/pi/mnt/USB_Cam_Mangeoire/Data_Raspi_Session.txt")        
    
    
    while Number_Of_Videos < 5000:
        
        Global_Iteration = Global_Iteration + 1 
        
        time.sleep(0.1)
        Number_Of_Videos=len(os.listdir("//home/pi/mnt/USB_Cam_Mangeoire/Video"))
        time.sleep(0.1)
        
        Send_String=""
               
       # this loop allows to discard bad received line by continuing if an error appears
        while 1:

           if ser.in_waiting:
               try:
                   Send_String=ser.readline().decode() # received data from esp32
                   Send_String = Send_String.replace('\0', '') # solving a bug that appears seomtimes
                   
               except:
                   print("Continue of ser.readline() triggered")
                   print(Send_String)
                   with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                       Data.write("Continue of ser.readline() triggered" + "\n" )
                       Data.write(Send_String + "\n")
                       
                   Global_Iteration = Global_Iteration - 1
                   continue
               break
 

 #sometimes the line is not correctly formated (bad receiving): the try catch 
 # allows to continue otherwise.
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

        
# sometimes the number of float is not correct. Continue if it appears.

        if len(floats) < 7 : #sometimes error due to floats size inf to 3
    
            print(len(floats))
          
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                  
                Data.write("Continue of LENGTH float triggered" + "\n" )
                Data.write(Send_String + "\n")
                Data.write("Lenght float: "+ str(len(floats)) + "\n")
            
            Global_Iteration = Global_Iteration - 1
                  
            continue

# parse all data from the esp32  sent line into float.
#                 
        Transistor_State=floats[0]
        Reboot_Reason=floats[1]
        Raspi_Voltage=floats[2]
        Raspi_Current=floats[3]   
        Solar_Current=floats[4]
        Current_Epoch=floats[5]
        Epoch_Start=floats[6]
        
        # specific log file that is removed when esp is reboot. the epoch 160000... is sent from 
        # esp32 and when set like that, it means that it just start ( the epoch 0  doesn't work
        # for unknown reasons)

        if Epoch_Start == 1600000000 and Global_Iteration == 1:
            
            if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt'):
                os.remove("//home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt") 
            
        #  to obtain data from the night (when raspi was off and esp32 continue monitoring data)
        if Transistor_State == 0 and Reboot_Reason > 0:
            Received_All_Transistor_Off_Data_from_ESP32(ser)
            
            print("Continue of Transistor_OFF_Transfert triggered")
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                Data.write("Continue of Transistor_OFF_Transfert triggered" + "\n" )
                
            ser.flushInput()
            
            continue
        
       # add somes informations in the line that gonna be write in the data text file.

        Send_String= str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ',' + \
                     str(round(datetime.datetime.now().timestamp()-Initial_T.timestamp(),2)) + ','\
                     + str(Number_Of_Videos) + ',' + str(Global_Iteration) + ','\
                     + Send_String 
        
        print(Send_String)
        
        # write the data line in the 3 logs files.

        with open("//home/pi/mnt/USB_Cam_Mangeoire/Data_All.txt","a")  as Data:
             Data.write(Send_String)
        
        with open("//home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt","a")  as Data:
             Data.write(Send_String)
             
             
        with open("//home/pi/mnt/USB_Cam_Mangeoire/Data_Raspi_Session.txt","a")  as Data:
             Data.write(Send_String)
        
        # shutdown the raspi if voltage reach the limit

        if Raspi_Voltage < (Voltage_Limit_To_Shutdown_Raspi) :            
            
            print("Entering the close condition due to Voltage limit measured at " + str(Raspi_Voltage) + " at "  + str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                 Data.write("Entering the close condition due to Voltage limit measured at " + str(Raspi_Voltage) + " at "  + str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))+ "\n" )
            
# Here we dont want that he send the real epoch_restart because we want that once the voltage is higher than 15.1
# the transistor is switch on again and allow raspi to reboot, not waiting that the time condition is reached. Thus
# I put 1600000001 that is a non sens epoch (that will always be lower than the current time; thus the condition that 
# the restart epoch is lower than the current epoch will always be reached)? Don't put 1600000000 because that remove
the esp log file (see condition above). 1600000001 should do the trick.

            Send_Epoch_To_Esp32(ser,1600000001)
            
            print("shutdown the pi in 10 sec")
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                 Data.write("shutdown the pi in 10 sec" + "\n" )
                 
            time.sleep(10)
            print("shutdown the pi")
            with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                 Data.write("shutdown the pi" + "\n" + "\n" )

            # not particularly beautifull but the only way to stop the python script
            # and allows to switch off the pi when launch from rc.local (root)

            run("sudo pkill -1 python3 ; sleep 10 ; sudo shutdown -h now", shell=True) # shutdown doesn't work without this command. dont know why.
            time.sleep(20)
        
# shutdown the raspi if the time limit is reached 

        elif round(time.time()) > epoch_to_stop:
            
            print("Entering the close condition due to Time limit  at " + str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " at voltage "+ str(Raspi_Voltage))
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
        
        
        time.sleep(1)
        Iteration_Of_Video=Get_Iteration_Of_Video() #based on iteration of the last modified file
        print(Iteration_Of_Video)
        Lead_Zero_Iteration=str(Iteration_Of_Video).zfill(5)
        video_name= "//home/pi/mnt/USB_Cam_Mangeoire/Video/video_" + Lead_Zero_Iteration + ".mp4"
        print(video_name)
        with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
            Data.write("Beginning " + video_name + " at " + str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " at voltage "+ str(Raspi_Voltage) + "\n" ) 
        
        # this ser flush is needed to avoid that serial buffer is filled if esp32 send data at a higher
        # rate (often the case; 10 sec vs  1minutes). Note that the time that gonna be keept maybe innacurate
        # at 1 minute of std.       
        ser.flushInput() 
        
        t = time.time()
        print("Acquiring video...")
        
# Change run by Popenif want that ffmpeg works in the background

        run([
        'ffmpeg',
        '-f', 'alsa',     #for sound
        '-channels', '1',
        '-thread_queue_size', '1024',
        '-i', 'plughw:2,0', #for sound

        '-f', 'v4l2', #for video input
#        '-thread_queue_size', '4096',
        '-s', resolution,
        '-i', '/dev/video0', #the video input (USB cam)
        
        '-r', str(Frame_Per_Second), # framerate (5 would be 5fps )
        '-t', str(Duration_of_Video), # time in second of video
        '-c:v', 'h264_omx', #raspi efficient hardware codec
        '-b:v', Bitrate, # the lowest, the highest compression but more bad quality
        video_name,
        '-y', #erase the file if aleady exist
        ],
        stdout=DEVNULL,# removing output in the terminal: comment if bug to see stdout
        stderr=STDOUT,
        #        stderr=DEVNULL,    
        )
        
        print("Time to take video:" + str(time.time()-t))

# create /home/pi/mnt with the path of internet box         
def Open_Shared_Folder():
        
    process = Popen(
        "sudo mount -t cifs //192.168.1.1/CleMichel /home/pi/mnt -o vers=1.0,username=pi,password=cardyna!",
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
    )
    
    time.sleep(1)# to avoid a print blanck line
    # code present on internet example to trow error if failed, i think
    while process.poll() is None:
        print(process.stdout.readline()) 

# allow to define a time to restart in absolute or relative way
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


# allow to define a time to stop in absolute or relative way
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

# usefull to detect the last modified file and use its name to found the next iteration 
# that shoudl be used.

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

# serial communication between esp32 and raspi are not always easy. This script
# send a message to the esp32 to tell it what time is it and when the transistor should
# be turn on again to switch on again the raspi. Since errors and bugs occurs, it is needed
# to check that the esp32 had received the epochs and send back aknowledgement. A double
# aknowledgement is also used for debugging purpose but probably became useless. the major
# part of this code is for debugging purpose and may probably be simplified. 

def Send_Epoch_To_Esp32(ser,epoch_to_restart):
        
    i = 0
    j = 0
    # the difficutly was to wait that esp32 awake from light sleep.
    ser.reset_input_buffer()
    while 1:
               
        if ser.in_waiting: #to avoid to do the ser.write during light sleep.
            
            Line=ser.readline().decode()

            # will try to send the two epochs untils the answer from esp32 is "Epoch received"
            while Line != "Epoch received\r\n":
                i = i+1
                Two_Epoch= "Epoch Sent," + str(round(time.time())) + ',' + str(epoch_to_restart ) + ','

                ser.write(Two_Epoch.encode())
                print("Break Sent:" + str(i))
                with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                      Data.write("Break Sent:" + str(i) + "\n")
                #time.sleep(8) #critical
                
                ser.reset_input_buffer()
                t = time.time()     
                while  ser.in_waiting < 1:
                        time.sleep(0.25)
                        
                
                print("Time in the while loop:" + str(time.time()-t))
                time.sleep(0.25) 
                Line=ser.readline().decode()
                print(Line)
                with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
                      Data.write(Line + "\n")
               
                ser.write("Double check OK".encode())
                
            break
        time.sleep(0.25)
        j=j+1
        print("j= " + str(j))
        # with open("//home/pi/mnt/USB_Cam_Mangeoire/Log.txt","a")  as Data:
        #               Data.write("j= " + str(j) + "\n")

#  rc.local launch the script as root (i may change this behaviour in the future). 
# there is complicated consequencies and when calling the script from thonny, i think, it's
# better to give all right to files to avoid errors (based on my memory unperfect)

def Authorize_To_Write_Files():



    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Data_All.txt'):

        call("sudo chmod 777 //home/pi/mnt/USB_Cam_Mangeoire/Data_All.txt", shell=True)

    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Log.txt'):
    
        call("sudo chmod 777 //home/pi/mnt/USB_Cam_Mangeoire/Log.txt", shell=True)
        
    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt'):
        
        call("sudo chmod 777 //home/pi/mnt/USB_Cam_Mangeoire/Data_ESP_Session.txt", shell=True)
        
        
    if os.path.isfile('//home/pi/mnt/USB_Cam_Mangeoire/Data_Raspi_Session.txt'):
        
        call("sudo chmod 777 //home/pi/mnt/USB_Cam_Mangeoire/Data_Raspi_Session.txt", shell=True)

# the complex serial communication to receive all data of the night (raspi off) from esp32
# when raspi boot. This function generates less bug that the one with the epoch.

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

# pythonic way to allow to put function below the main script.

if __name__ == '__main__':
    main()



  
#command='ffmpeg -f v4l2 -r 5 -s 1920x1080 -input_format yuyv422 -i /dev/video0 -t 100 -r 5 -c:v libx264 -crf 23 -preset ultrafast -vf format=yuv420p  /home/pi/mnt/USB_Cam_Mangeoire/out.mp4 -y'
#command='ffmpeg -f v4l2 -input_format mjpeg -r 5 -s 1920x1080 -input_format yuyv422 -i /dev/video0 -t 15 -r 1 -c:v h264_omx /home/pi/mnt/USB_Cam_Mangeoire/out.mp4 -y'
#command='ffmpeg -f v4l2  -input_format yuyv422  -r 5 -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 16M /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
#command='ffmpeg -f v4l2  -input_format mjpeg  -r 20 -s 1920x1080 -i /dev/video0 -t 30 -r 20 -c:v copy  /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
#command='ffmpeg  -i /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4  -c:v h264_omx  -b:v 16M  /home/pi/mnt/USB_Cam_Mangeoire/out_MJPEG_Then_OMX.mp4 -y'
#command='ffmpeg -ar 44100 -ac 1 -f alsa  -i plughw:2,0 -f v4l2  -input_format yuyv422  -r 5 -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 8M -acodec aac /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'
#command='ffmpeg -f alsa  -i plughw:2,0 -f v4l2  -s 1920x1080 -i /dev/video0 -t 30 -r 1 -c:v h264_omx  -b:v 8M -acodec libmp3lame /home/pi/mnt/USB_Cam_Mangeoire/out_16M.mp4 -y'

