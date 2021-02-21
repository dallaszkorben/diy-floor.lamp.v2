from time import sleep

#if __name__ == "__main__":
#    from sa import SA
#    from sa_pwm import SAPwm
#    from sa_ky040 import SAKy040
#
#else:
from senact.sa_pwm import SAPwm
from senact.sa_ky040 import SAKy040
from egadget.eg import EG

#if __name__ == "__main__":
#    import os
#    import sys
#
#    currentdir = os.path.dirname(os.path.realpath(__file__))
#    parentdir = os.path.dirname(currentdir)
#    sys.path.append(parentdir)
#
#    from senact.sa_pwm import SAPwm
#    from senact.sa_ky040 import SAKy040
#
#else:
#    from senact.sa_pwm import SAPwm
#    from senact.sa_ky040 import SAKy040

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

        print( "reset - ", str(lightValue['current']))

    def rotaryChanged(self, value):

        lightValue = self.fetchLightValue()

        newValue = lightValue['current'] + value

        if newValue > EGLight.POTMETER_MAX:
            newValue = EGLight.POTMETER_MAX
        elif newValue < EGLight.POTMETER_MIN:
            newValue = EGLight.POTMETER_MIN

        self.setLight(newValue, newValue)

        print( "turned - ", str(newValue))

    def switchPressed(self):
        lightValue = self.fetchLightValue()

        if lightValue['current']:
            newValue = EGLight.POTMETER_MIN
            turned = "off"
            self.setLight(newValue, lightValue['current'])

        else:
#            newValue = self.__class__.POTMETER_MAX
            newValue = lightValue['before-off']
            turned = "on"
            self.setLight(newValue, newValue)

        print ("button pressed - turned", turned, "(", newValue, ")")

    # save the value and change the level of the light
    def setLight(self, lightValue, lightBeforeOff=100):
        self.saveLightValue(lightValue, lightBeforeOff)
        pwmValue = self.saPwm.setPwmByValue(lightValue)

    def setLightGradually(self, actuator, fromValue, toValue, inSeconds):
        pwmValue = self.saPwm.setPwmByStepValueGradually(actuator, fromValue, toValue, inSeconds)
        self.saveLightValue(toValue)


