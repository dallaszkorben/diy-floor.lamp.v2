#! /usr/bin/python3

from datetime import datetime
from datetime import timedelta
import tzlocal

#from datetime import timedelta

import requests

from time import sleep

if __name__ == "__main__":

    r = requests.post("http://localhost:5000/gradually/set", data={'actuator': '1', 'value': '4', 'inSeconds': '1'})
    print(r.text)

    timeZone = tzlocal.get_localzone()
    nowDateTime=datetime.now().astimezone(timeZone).replace(microsecond=0)
    plus5secondsDateTime = nowDateTime + timedelta(seconds = 5)

    r = requests.post("http://localhost:5000/gradually/schedule/set", data={'actuator': '1', 'value': '100', 'inSeconds': '10', 'at': plus5secondsDateTime.isoformat()})
    print(r.text)
