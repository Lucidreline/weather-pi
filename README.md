# Weather Pi

## Installation

Python version 3.6.9

### Config

Create a env.py folder in the root folder of the project (next to app.py).

Add your customized values to the following variables

```python
  comfortableTemp = 65 # this will be the value of the middle light
  lightTemperatureInterval = 10  # the temperature difference between each light

  haveLedLights = True # weather you have a raspberry pi and led lights connected
  lightPinNumbers = [22, 27, 17, 18, 4] # the number of the gpio pins connected to the raspberry pi
```

### Dependencies

```bash
pip3 install requests schedule
```
