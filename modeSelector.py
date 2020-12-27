from requests import get
import config


class ModeSelector:
    def __init__(self):
        self.mode = 1
        self.numOfModes = 1

    def tranverseModes(self):  # a button on the breadboard will call this
        self.mode += 1
        if self.mode > self.numOfModes:
            self.mode = 1

        self.modeSelector(self.mode)

    def modeSelector(self, modeNumber):
        if modeNumber == 1:
            self.temperatureMode()

    # displays the temperature using 5 lights and their brightness
    def temperatureMode(self):
        # grab the current temperature from the best weather api on the world wide web :)
        currentTemperature = get(
            'https://rainbarrel.manuelc.me/api/current').json()['temp_F']

        # create a list of lights where the middle light is the comfortable temperature and each light has a set interval
        firstLightBrightness = config.comfortableTemp - \
            (config.lightTemperatureInterval * 2)
        lightTemps = []

        for i in range(5):
            lightTemps.append(firstLightBrightness +
                              (i * config.lightTemperatureInterval))
            # if comfortableTemp = 65 & interval = 10, then lightTemps = [45, 55, 65, 75, 85]

        print(lightTemps)

        # light temperatures: 45 55 65 75 85
        # tests cases:
        # 65 -> [0 0 100 0 0]  | if the degrees matches a light tempertature exactly, that light will be at 100% brightness
        # 70 -> [0 0 50 50 0]  | if the degrees is in the middle of two lights, the two lights will be at 50%
