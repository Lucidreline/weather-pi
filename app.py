import time

import env
from modeSelector import ModeSelector

if env.haveLedLights:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(env.btnPinNumber, GPIO.IN, pull_up_down=GPIO.PUD_UP)


selector = ModeSelector()  # creates instance of the mode selector class

modeButtonPushed = False

transverseRate = 0.75  # how many seconds to wait after transversing again
timeToTransverse = 0.0  # reinforces the transverseRate


while True:
    time.sleep(0.1)

    if env.haveLedLights:

        # check if there is button input
        if GPIO.input(env.btnPinNumber) == False and int(time.time()) > timeToTransverse:
            timeToTransverse = int(time.time()) + 1
            selector.tranverseModes()
        else:
            selector.continueMode()

    else:
        selector.continueMode()
