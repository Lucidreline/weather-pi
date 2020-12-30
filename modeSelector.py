from requests import get
from datetime import datetime

from lights import LightingSystem
import config


class ModeSelector:
    def __init__(self):
        self.mode = 1
        self.numOfModes = 1

        self.keepRefreshing = True

        self.lights = LightingSystem()

        self.modeSelector(self.mode)

    def continueMode(self):
        # prevents me from sending myself too many api calls
        if datetime.now().minute == 25 and self.keepRefreshing:
            self.keepRefreshing = False
            self.modeSelector(self.mode)
        elif datetime.now().minute != 25:
            self.keepRefreshing = True

    def tranverseModes(self):  # a button on the breadboard will call this
        # incase the button is pushed before the keepRefreshing variable is turned back into True
        self.keepRefreshing = True

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
        updatedLights = [0, 0, 0, 0, 0]

        if currentTemperature <= lightTemps[0]:
            updatedLights[0] = 100
        elif currentTemperature >= lightTemps[len(lightTemps) - 1]:
            updatedLights[len(updatedLights) - 1] = 100
        else:
            for i in range(1, len(lightTemps)):  # starts index at 1
                if currentTemperature <= lightTemps[i]:

                    # lets say the previous light temp was 55, then temperature is 60, and the current light temp is 65
                    # we take the previous light temp (55) and subtract that from the other two values, so
                    # we get a temperature of 5, and a current light temp of 10
                    # then divide the temperature by current light temp (5/10), and you get your current light percentage
                    # multiply it by 100 so that it goes from decimal to percent (0.5 -> 50)
                    # to get the previous light percent brightness, subtract 100 - the previous percentage (50)

                    subtractedCurrentLightTemp = lightTemps[i] - \
                        lightTemps[i-1]
                    subtractedCurrentTemperature = currentTemperature - \
                        lightTemps[i-1]

                    currentLightBrightness = (
                        subtractedCurrentTemperature / subtractedCurrentLightTemp) * 100
                    previousLightBrightness = 100 - currentLightBrightness

                    updatedLights[i] = currentLightBrightness
                    updatedLights[i - 1] = previousLightBrightness

                    break

        self.lights.updateLights(updatedLights)

        # test light temperatures: 45 55 65 75 85
        # tests cases:
        # 65 -> [0 0 100 0 0]  | if the degrees matches a light tempertature exactly, that light will be at 100% brightness
        # 70 -> [0 0 50 50 0]  | if the degrees is in the middle of two lights, the two lights will be at 50%
        # 40 -> [100 0 0 0 0]  | if the degrees out of range, make the closest light to it 100% brightness
