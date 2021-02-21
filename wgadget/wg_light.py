from datetime import datetime
import tzlocal
import time

import json
from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

#from webgadget.representations import output_json
from wgadget.immediately import ImmediatelyView
from wgadget.gradually import GraduallyView

from threading import Thread

from egadget.eg_light import EGLight

from config.config_exchange import getConfigExchange
from config.config_exchange import setConfigExchange
from config.config_egadget import getConfigEGadget

class WGLight(object):

    def __init__(self, gadgetName, actuatorLightId, pinPwm, freqPwm, sensorPotmeterId, pinClock, pinData, pinSwitch):

        cg = getConfigEGadget()

        try:
            self.POTMETER_MIN = int(cg["potmeter-min"])
        except(ValueError):
            self.POTMETER_MIN = 0
        try:
            self.POTMETER_MAX = int(cg["potmeter-max"])
        except(ValueError):
            self.POTMETER_MAX = 100
        try:
            self.POTMETER_STEP = cg["potmeter-min"]
        except(ValueError):
            self.POTMETER_STEP = 1

        self.gadgetName = gadgetName
        self.actuatorLightId = actuatorLightId
        self.sensorPotmeterId = sensorPotmeterId

        self.egLight = EGLight( gadgetName, actuatorLightId, pinPwm,  freqPwm, sensorPotmeterId, pinClock, pinData, pinSwitch, self.fetchLightValue, self.saveLightValue )

        self.app = Flask(__name__)

        # register the end-points
#        self.ConfigSomethingView.register(self.app, init_argument=self)
        ImmediatelyView.register(self.app, init_argument=self)
        GraduallyView.register(self.app, init_argument=self)

    def getLightId(self):
        return self.actuatorLightId

    def getPotmeterId(self):
        return self.sensorPotmeterId

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

#if __name__ == "__main__":
#
#    PIN_PWM = 18
#    FREQ_PWM = 800
#
#    PIN_CLOCK = 17
#    PIN_DATA = 27
#    PIN_SWITCH = 23
#
#    GADGET_NAME = "Light"
#    ACTUATOR_LIGHT_ID = "1"
#    SENSOR_POTMETER_ID = "1"
#
#    wgLight = WGLight( GADGET_NAME, ACTUATOR_LIGHT_ID, PIN_PWM, FREQ_PWM, SENSOR_POTMETER_ID, PIN_CLOCK, PIN_DATA, PIN_SWITCH )
#
#    try:
#        wgLight.run(host= '0.0.0.0')
#    finally:
#        wgLight.unconfigure()
