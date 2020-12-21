from requests import get as req
import schedule
import time


def job():
    currentWeather = req('http://rainbarrel.manuelc.me/api/current').json()
    print(currentWeather)


schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
