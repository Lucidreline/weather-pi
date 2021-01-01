from datetime import datetime

import env

if env.haveLedLights:
    import RPi.GPIO as GPIO


class LightingSystem:
    def __init__(self):
        self.haveLights = env.haveLedLights
        self.centerLightPins = env.CenterlightPinNumbers
        self.rightLightPin = env.rightLightPinNumber
        self.lights = []

        if self.haveLights:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)

        # sets up the center lights
        for pinNum in self.centerLightPins:
            if self.haveLights:
                GPIO.setup(pinNum, GPIO.OUT)

            self.lights.append(Light(pinNum))

        # sets up the right light
        if self.haveLights:
            GPIO.setup(self.rightLightPin, GPIO.OUT)

        self.lights.append(Light(self.rightLightPin))

    def turnAllOff(self):
        for light in self.lightBrightnesses:
            light = 0

    def updateLights(self, updatedLightBrightness):

        for i in range(len(self.lights)):
            self.lights[i].updateBrightness(updatedLightBrightness[i])

        self.printLightBrightnesses()

    def printLightBrightnesses(self):
        print('Light Brightnesses at: ')
        print(datetime.now())
        lights = []

        for light in self.lights:
            lights.append(light.brightness)

        print(lights)
        print()


class Light:
    def __init__(self, pinNumber, startingBrightness=0):
        self.pinNumber = pinNumber
        self.brightness = startingBrightness

        if env.haveLedLights:
            self.pwm = GPIO.PWM(pinNumber, 100)

        self.updateBrightness(self.brightness)

    def updateBrightness(self, brightness):
        self.brightness = brightness

        if env.haveLedLights:
            self.pwm.start(self.brightness)
