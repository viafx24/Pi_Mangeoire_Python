import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.io


PinInputSDA=4
PinInputSCL=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(PinInputSDA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PinInputSCL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

LengthData=500000

DataSDA=np.zeros(LengthData)
DataSCL=np.zeros(LengthData)

t = time.time() # pay attention, it's not the equivalent to tic toc
for x in range(LengthData):
#     print(GPIO.input(4))
    DataSDA[x]=GPIO.input(PinInputSDA)
    DataSCL[x]=GPIO.input(PinInputSCL)

elapsed = time.time() - t

print(elapsed)

plt.plot(DataSDA,'b-')
plt.plot(DataSCL,'r-')
plt.show()


scipy.io.savemat('I2C_Two_Channel.mat', dict(DataSDA=DataSDA, DataSCL=DataSCL))


# fig, axs = plt.subplots(2)
# fig.suptitle('Vertically stacked subplots')
# axs[0].plot(DataSDA,'b-')
# axs[1].plot(DataSCL,'r-')
# plt.show()