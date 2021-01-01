from time import sleep

import env
from modeSelector import ModeSelector

if env.haveLedLights:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(env.btnPinNumber, GPIO.IN, pull_up_down=GPIO.PUD_UP)


selector = ModeSelector()  # creates instance of the mode selector class

modeButtonPushed = False

while True:
    sleep(0.1)

    if env.haveLedLights:

        # check if there is button input
        if GPIO.input(env.btnPinNumber) == False:
            selector.tranverseModes()
        else:
            selector.continueMode()

    else:
        selector.continueMode()
