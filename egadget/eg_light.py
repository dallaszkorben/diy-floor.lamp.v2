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

    def getSensor(self, id):
        if id == self.sensorId:
            return self.saKy040
        else:
            raise AttributeError("id={id} is not a valid ID")

    def getActuator(self, id):
        if id == self.actuatorId:
            return self.saPwm
        else:
            raise AttributeError("id={id} is not a valid ID")

    def getSensorIds(self):
        return (self.sensorId, )

    def getActuatorIds(self):
        return (self.actuatorId, )

    def resetLight(self):
        lightValue = self.fetchLightValue()
        self.setLight(lightValue)

        print( "reset - ", str(lightValue))

    def rotaryChanged(self, value):

        lightValue = self.fetchLightValue()
        lightValue += value

        if lightValue > self.__class__.POTMETER_MAX:
            lightValue = self.__class__.POTMETER_MAX
        elif lightValue < self.__class__.POTMETER_MIN:
            lightValue = self.__class__.POTMETER_MIN
#        self.saveLightValue(lightValue)

        self.setLight(lightValue)

        print( "turned - ", str(lightValue))

    def switchPressed(self):
        lightValue = self.fetchLightValue()
        if lightValue:
            lightValue = self.__class__.POTMETER_MIN
            turned = "off"
        else:
            lightValue = self.__class__.POTMETER_MAX
            turned = "on"

        self.setLight(lightValue)

        print ("button pressed - turned", turned)

    # save the value and change the level of the light
    def setLight(self, value):
        self.saveLightValue(value)
        pwmValue = self.saPwm.setPwmByValue(value)

    def setLightGradually(self, actuator, fromValue, toValue, inSeconds):
        pwmValue = self.saPwm.setPwmByStepValueGradually(actuator, fromValue, toValue, inSeconds)
        self.saveLightValue(toValue)


