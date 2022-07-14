import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
import time


PinInput=4

GPIO.setmode(GPIO.BCM)
GPIO.setup(PinInput, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

LengthData=1000000


Data=np.zeros(LengthData)

t = time.time() # pay attention, it's not the equivalent to tic toc
for x in range(LengthData):
#     print(GPIO.input(4))
    Data[x]=GPIO.input(PinInput)

elapsed = time.time() - t

print(elapsed)

plt.plot(Data,'-')
plt.show()
