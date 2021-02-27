from time import sleep
import logging

from senact.sa_pwm import SAPwm
from senact.sa_ky040 import SAKy040
from egadget.eg import EG

class EGLight(EG):

    POTMETER_MIN = 0
    POTMETER_MAX = 100

    def __init__(self, gadgetName, actuatorId, pinPwm, freqPwm, sensorId, pinClock, pinData, pinSwitch, fetchLightValue, saveLightValue):

        self.gadgetName = gadgetName

        self.actuatorId = actuatorId
        self.pinPwm = pinPwm
        self.freqPwm = freqPwm

        self.sensorId = sensorId
        self.pinClock = pinClock
        self.pinData = pinData
        self.pinSwitch = pinSwitch

        self.fetchLightValue = fetchLightValue
        self.saveLightValue = saveLightValue

        self.saPwm = SAPwm(actuatorId, pinPwm, freqPwm)
        self.saKy040 = SAKy040(sensorId, pinClock, pinData, pinSwitch, self.rotaryChanged, self.switchPressed)

        self.saPwm.configure()
        self.saKy040.configure()

        self.resetLight()

    def getSensor(self, actuatorId):
        if actuatorId == self.sensorId:
            return self.saKy040
        else:
            raise AttributeError("actuatorId={actuatorId} is not a valid ID")

    def getActuator(self, actuatorId):
        if actuatorId == self.actuatorId:
            return self.saPwm
        else:
            raise AttributeError("actuatorId={actuatorId} is not a valid ID")

    def getSensorIds(self):
        return (self.sensorId, )

    def getActuatorIds(self):
        return (self.actuatorId, )

    def resetLight(self):
        lightValue = self.fetchLightValue()

        if lightValue['current']:
            self.setLight(lightValue['current'], lightValue['current'])
        else:
            self.setLight(lightValue['current'], 100)

        logging.info("Reset:          " + str(lightValue['current']))

    def rotaryChanged(self, value):

        lightValue = self.fetchLightValue()

        newValue = lightValue['current'] + value

        if newValue > EGLight.POTMETER_MAX:
            newValue = EGLight.POTMETER_MAX
        elif newValue < EGLight.POTMETER_MIN:
            newValue = EGLight.POTMETER_MIN

        self.setLight(newValue, newValue)

    def switchPressed(self):
        lightValue = self.fetchLightValue()

        if lightValue['current']:
            newValue = EGLight.POTMETER_MIN
            turned = "off"
            self.setLight(newValue, lightValue['current'])

        else:
            newValue = lightValue['before-off']
            turned = "on"
            self.setLight(newValue, newValue)

    # save the value and change the level of the light
    def setLight(self, lightValue, lightBeforeOff=100):
        self.saveLightValue(lightValue, lightBeforeOff)

        if lightValue:
            logging.info( "Set Light to {0} in {1})".format(
                lightValue,
                __file__)
            )

        else:
            logging.info( "Set Light to {0} from {1} --- FILE: {2}".format(
                lightValue,
                lightBeforeOff,
                __file__)
            )

        pwmValue = self.saPwm.setPwmByValue(lightValue)


    def setLightGradually(self, actuator, fromValue, toValue, inSeconds):

        logging.info( "Set Light to {0} from {1} in {2} seconds --- FILE: {3}".format(
            toValue,
            fromValue,
            inSeconds,
            __file__)
        )

        pwmValue = self.saPwm.setPwmByStepValueGradually(actuator, fromValue, toValue, inSeconds)
        self.saveLightValue(toValue)



