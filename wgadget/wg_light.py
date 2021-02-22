
import os
import logging
from logging.handlers import RotatingFileHandler

from datetime import datetime
import tzlocal
import time

import json
from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from wgadget.immediately import ImmediatelyView
from wgadget.gradually import GraduallyView

from threading import Thread

from egadget.eg_light import EGLight

from config.config_exchange import getConfigExchange
from config.config_exchange import setConfigExchange
from config.config_egadget import getConfigEGadget

from config.config_location import ConfigLocation

class WGLight(object):

#    def __init__(self, gadgetName, actuatorLightId, pinPwm, freqPwm, sensorPotmeterId, pinClock, pinData, pinSwitch):
    def __init__(self):
        cg = getConfigEGadget()

        self.gadgetName = cg["gadget-name"]
        logLevel = cg["log-level"]
        logFileName = cg["log-file-name"]
        self.actuator1Id = cg["actuator-1-id"]
        self.actuator1PwmPin = cg["actuator-1-pin"]
        self.actuator1PwmFreq = cg["actuator-1-freq"]
        self.actuator1PwmMinDutyCycle = cg["actuator-1-min-duty-cycle"]
        self.actuator1PwmMaxDutyCycle = cg["actuator-1-max-duty-cycle"]
        self.sensor1Id = cg["sensor-1-id"]
        self.sensor1Min = cg["sensor-1-min"]
        self.sensor1Max = cg["sensor-1-max"]
        self.sensor1Step = cg["sensor-1-step"]
        self.sensor1ClockPin = cg["sensor-1-clock-pin"]
        self.sensor1DataPin = cg["sensor-1-data-pin"]
        self.sensor1SwitchPin = cg["sensor-1-switch-pin"]

        # LOG 
        logFolder = ConfigLocation.get_path_to_config_folder()
        logPath = os.path.join(logFolder, logFileName)
        logging.basicConfig(
            handlers=[RotatingFileHandler(logPath, maxBytes=5*1024*1024, backupCount=5)],
            format='%(asctime)s %(levelname)8s - %(message)s' , 
            level = logging.ERROR if logLevel == 'ERROR' else logging.WARNING if logLevel == 'WARNING' else logging.INFO if logLevel == 'INFO' else logging.DEBUG if logLevel == 'DEBUG' else 'CRITICAL' )

        self.egLight = EGLight( self.gadgetName, self.actuator1Id, self.actuator1PwmPin, self.actuator1PwmFreq, self.sensor1Id, self.sensor1ClockPin, self.sensor1DataPin, self.sensor1SwitchPin, self.fetchLightValue, self.saveLightValue )

        self.app = Flask(__name__)

        # register the end-points
        ImmediatelyView.register(self.app, init_argument=self)
        GraduallyView.register(self.app, init_argument=self)

    def getLightId(self):
        return self.actuator1Id

    def getPotmeterId(self):
        return self.sensor1Id

    def unconfigure(self):
        self.egLight.unconfigure()

    def run(self, host='0.0.0.0'):
        self.app.run(host=host)

    def setLight(self, value, beforeOffValue=100):
        self.egLight.setLight(value, beforeOffValue)

    def reverseLight(self):
        self.egLight.switchPressed()

    def setLightGradually(self, actuator, fromValue, toValue, inSeconds):
        self.egLight.setLightGradually(actuator, fromValue, toValue, inSeconds)

    def setLightScheduledGradually(self, actuator, toValue, inSeconds, atDateTime):

        timeZone = tzlocal.get_localzone()
        zoneName = timeZone.zone

        atDateTime=atDateTime.astimezone(timeZone).replace(microsecond=0)

        while True:
            time.sleep(1)
            nowDateTime=datetime.now().astimezone(timeZone).replace(microsecond=0)
            if nowDateTime >= atDateTime:
                break

        fromValue = self.fetchLightValue()
        self.egLight.setLightGradually(actuator, fromValue['current'], toValue, inSeconds)

    def fetchLightValue(self):
        config_ini = getConfigExchange()

        return {
            'current': int(config_ini["light-current-value"]),
            'before-off': int(config_ini["light-before-off-value"])
        }

    def saveLightValue(self, value, beforeOffValue=100):

        config_ini = getConfigExchange()
        config_ini["light-current-value"] = value
        if value:
            config_ini["light-before-off-value"] = value
        else:
            config_ini["light-before-off-value"] = beforeOffValue

        setConfigExchange(config_ini)

