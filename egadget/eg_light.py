from time import sleep
import logging

from senact.sa_pwm import SAPwm
from senact.sa_ky040 import SAKy040
from egadget.eg import EG

class EGLight(EG):

    def __init__(self, gadgetName, actuatorPwm, sensorKy040, fetchSavedLightValue=None, saveLightValue=None, rotaryCallbackMethod=None, switchCallbackMethod=None):

        self.minLightValue = 30
        self.maxLightValue = 80

        self.gadgetName = gadgetName

        self.actuatorPwm = actuatorPwm
        self.sensorKy040 = sensorKy040

        if rotaryCallbackMethod:
            self.sensorKy040.setRotaryCallbackMethod(rotaryCallbackMethod)
        else:
            self.sensorKy040.setRotaryCallbackMethod(self.rotaryCallbackMethod)

        if switchCallbackMethod:
            self.sensorKy040.setSwitchCallbackMethod(switchCallbackMethod)
        else:
            self.sensorKy040.setSwitchCallbackMethod(self.switchCallbackMethod)

        self.fetchSavedLightValue = fetchSavedLightValue
        self.saveLightValue = saveLightValue

        self.actuatorPwm.configure()
        self.sensorKy040.configure()

        self.resetLight()

    def getGadgetName(self):
        return self.gadgetName

    def getSensor(self, sensorId):
        if sensorId == self.sensorKy040.id:
            return self.sensorKy040
        else:
            raise AttributeError(f"sensorId={sensorId} is not a valid ID")

    def getSensorKy040(self):
        return self.sensorKy040

    def getActuator(self, actuatorId):
        if actuatorId == self.actuatorPwm.id:
            return self.actuatorPwm
        else:
            raise AttributeError(f"actuatorId={actuatorId} is not a valid ID")

    def getActuatorPwm(self):
        return self.actuatorPwm

    def getSensorIds(self):
        return (self.sensorKy040.id, )

    def getActuatorIds(self):
        return (self.actuatorPwm.id, )

    def resetLight(self):

        if self.fetchSavedLightValue:
            lightValue = self.fetchSavedLightValue()
        else:
            self.lightValue = {'current': self.minLightValue, 'previous': self.maxLightValue}
            lightValue = self.lightValue

        self.setLight(lightValue['current'], lightValue['previous'])

        logging.info("Reset:          current:{0}, previous:{1}".format(lightValue['current'], lightValue['previous']))

    def setLight(self, newLightValue, oldLightValue=None) -> dict:
        """
        Saves the value and change the level of the light 
        """

        if self.saveLightValue:
            self.saveLightValue(newLightValue, oldLightValue)
        else:
            if oldLightValue:
                self.lightValue['previous'] = oldLightValue
            else:
                self.lightValue['previous'] = self.lightValue['current']

            self.lightValue['current'] = newLightValue

        pwmValue = self.actuatorPwm.setPwmByValue(newLightValue)

        logging.info( "Set Light to {0} --- FILE: {1}".format(
            newLightValue,
            __file__)
        )

        return {'result': 'OK', 'value': newLightValue}

    def setLightGradually(self, actuator, fromValue, toValue, inSeconds):

        pwmValue = self.actuatorPwm.setPwmByStepValueGradually(actuator, fromValue, toValue, inSeconds)

        logging.info( "Set Light {0} -> {1} in {2} seconds --- FILE: {3}".format(
            fromValue,
            toValue,
            inSeconds,
            __file__)
        )

        if self.saveLightValue:
            self.saveLightValue(toValue, fromValue)
        else:
            self.lightValue['previous'] = fromValue
            self.lightValue['current'] = toValue

        return {'result': 'OK', 'value': toValue}



    # ==============================================

    def rotaryCallbackMethod(self, value) -> dict:

        if self.fetchSavedLightValue:
            lightValue = self.fetchSavedLightValue()
        else:
            lightValue = self.lightValue

        newValue = lightValue['current'] + value

        if newValue > self.maxLightValue:
            newValue = self.maxLightValue
        elif newValue < self.minLightValue:
            newValue = self.minLightValue

        return self.setLight(newValue)

    def switchCallbackMethod(self) -> dict:

        if self.fetchSavedLightValue:
            lightValue = self.fetchSavedLightValue()
        else:
            lightValue = self.lightValue

        if lightValue['current']:
            newValue = self.minLightValue
            turned = "off"

        else:
            newValue = lightValue['previous']
            turned = "on"

        return self.setLight(newValue)

    # ================================================
