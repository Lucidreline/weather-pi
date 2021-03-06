from requests import get
from datetime import datetime

from lights import LightingSystem
import env


class ModeSelector:
    def __init__(self):
        self.modes = [self.temperatureMode, self.comparedToYesterdayMode]
        self.mode = 0
        self.modeLightBrightness = 0

        self.keepRefreshing = True

        self.lights = LightingSystem()

        self.modeSelector(self.mode)

    def continueMode(self):

        timeToRefresh = datetime.now().minute % env.updateFreqMins == 0

        # prevents me from sending myself too many api calls
        if timeToRefresh and self.keepRefreshing:
            self.keepRefreshing = False
            self.modeSelector(self.mode)
        elif not timeToRefresh:
            self.keepRefreshing = True

    def tranverseModes(self):  # a button on the breadboard will call this
        # incase the button is pushed before the keepRefreshing variable is turned back into True
        self.keepRefreshing = True

        self.mode += 1
        if self.mode > len(self.modes) - 1:
            self.mode = 0

        self.modeSelector(self.mode)

    def modeSelector(self, modeNumber):
        self.modes[modeNumber]()

    def getModeLightBrightness(self):
        return self.mode / (len(self.modes) - 1)

    # displays the temperature using 5 lights and their brightness
    def temperatureMode(self):
        print('Mode: Current Temperature')
        # grab the current temperature from the best weather api on the world wide web :)
        currentTemperature = get(
            'https://rainbarrel.manuelc.me/api/current').json()['temp_F']

        # create a list of lights where the middle light is the comfortable temperature and each light has a set interval
        firstLightBrightness = env.comfortableTemp - \
            (env.lightTemperatureInterval * 2)
        lightTemps = []

        for i in range(5):
            lightTemps.append(firstLightBrightness +
                              (i * env.lightTemperatureInterval))
            # if comfortableTemp = 65 & interval = 10, then lightTemps = [45, 55, 65, 75, 85]
        # every light will be atleast 1% brightness
        updatedLightBrightnesses = [
            1, 1, 1, 1, 1, self.getModeLightBrightness()]

        if currentTemperature <= lightTemps[0]:
            updatedLightBrightnesses[0] = 100
        elif currentTemperature >= lightTemps[len(lightTemps) - 1]:
            updatedLightBrightnesses[len(updatedLightBrightnesses) - 1] = 100
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

                    updatedLightBrightnesses[i] = currentLightBrightness
                    updatedLightBrightnesses[i - 1] = previousLightBrightness

                    break

        self.lights.updateLights(updatedLightBrightnesses)

        # test light temperatures: 45 55 65 75 85
        # tests cases:
        # 65 -> [0 0 100 0 0]  | if the degrees matches a light tempertature exactly, that light will be at 100% brightness
        # 70 -> [0 0 50 50 0]  | if the degrees is in the middle of two lights, the two lights will be at 50%
        # 40 -> [100 0 0 0 0]  | if the degrees out of range, make the closest light to it 100% brightness

    # displays how much colder or hotter it is compared to yesterday
    def comparedToYesterdayMode(self):
        print('Mode: Compared To Yesterday')
        self.lights.updateLights(
            [20, 40, 60, 80, 100, self.getModeLightBrightness()])
