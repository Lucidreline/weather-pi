
class Lights:
    def __init__(self):
        self.lightBrightnesses = [0, 0, 0, 0, 0]

    def turnAllOff(self):
        for light in self.lightBrightnesses:
            light = 0

    def updateLights(self):
        for light in self.lightBrightnesses:
            print(light)
        # write
