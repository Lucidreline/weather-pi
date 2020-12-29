from time import sleep

from modeSelector import ModeSelector

selector = ModeSelector()  # creates instance of the mode selector class

modeButtonPushed = False

while True:
    sleep(0.1)

    # check if there is button input
    if modeButtonPushed:
        selector.tranverseModes()
    else:
        selector.continueMode()
