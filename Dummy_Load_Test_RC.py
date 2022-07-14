import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from ina219 import INA219
from ina219 import DeviceRangeError
import time
import numpy as np


def animate(i,y1,y2):

    Voltage = ina.voltage()
    Current = ina.current()
             
    print("Bus Voltage: %.3f V" % ina.voltage())
    print("Bus Current: %.3f mA" % ina.current())
#     print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
#     print("Supply voltage: %.3f V" % ina.supply_voltage())
    
    y1.append(Voltage)
    y2.append(Current)

    y1=y1[-x_len:]
    y2=y2[-x_len:]

    line1.set_ydata(y1)
    line2.set_ydata(y2)


    return line1,line2,

try:
    
    SHUNT_OHMS = 0.1

    ina = INA219(SHUNT_OHMS,address=0x41)
    ina.configure()

    x_len = 200         # Number of points to display
    y_range_Voltage = [0, 20]  # Range of possible Y values to display
    y_range_Current = [0, 4000]

    fig, (ax1,ax2) = plt.subplots(2, 1)
    ax1.set_title('Multimeter')
    ax1.set_ylabel('Voltage')
    ax2.set_ylabel('Current')
    ax2.set_xlabel('Frames')

    ax1.set_ylim(y_range_Voltage)
    ax2.set_ylim(y_range_Current)

    x1 = list(range(0, 200))
    y1 = [0] * x_len
    y2 = [0] * x_len

    line1, = ax1.plot(x1,y1,'b')
    line2, = ax2.plot(x1,y2,'r')
    
    #GPIO.setwarnings(False)			#disable warnings
    GPIO.setmode(GPIO.BOARD)		#set pin numbering system

    PWMpin = 7			# 
    GPIO.setup(PWMpin,GPIO.OUT)

    pi_pwm = GPIO.PWM(PWMpin,1000)		#create PWM instance with frequency
    pi_pwm.start(100)             

    #time.sleep(20)

    ani = animation.FuncAnimation(fig,
        animate,
        fargs=(y1, y2, ),
        interval=50,
        blit=True)
    plt.show()

except:
    
    print("Exception occurred...")
    
finally:
    
    pi_pwm.stop()
    GPIO.cleanup()
    print("but has cleanup GPIO")





