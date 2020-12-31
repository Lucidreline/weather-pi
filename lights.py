import env

if env.haveLedLights:
    import RPi.GPIO as GPIO


class LightingSystem:
    def __init__(self):
        self.haveLights = env.haveLedLights
        self.lightPinNumbers = env.lightPinNumbers
        self.lights = []

        if self.haveLights:
            GPIO.setmode(GPIO.BCM)

        for pinNum in self.lightPinNumbers:
            if self.haveLights:
                GPIO.setup(pinNum, GPIO.OUT)

            self.lights.append(Light(pinNum))

    def turnAllOff(self):
        for light in self.lightBrightnesses:
            light = 0

    def updateLights(self, updatedLightBrightness):

        for i in range(len(self.lights)):
            self.lights[i].updateBrightness(updatedLightBrightness[i])

        self.printLightBrightnesses()

    def printLightBrightnesses(self):
        print('Light Brightnesses')

        for light in self.lights:
            print(light.brightness)

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
