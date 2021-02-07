from time import sleep

#if __name__ == "__main__":
#    from sa import SA
#    from sa_pwm import SAPwm
#    from sa_ky040 import SAKy040
#
#else:
from senact.sa_pwm import SAPwm
from senact.sa_ky040 import SAKy040
from senact.sa import SA

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

class SALight(SA):

    POTMETER_MIN = 0
    POTMETER_MAX = 100

    ACTUATOR_LIGHT_ID = '1'

    def __init__(self, pinPwm, freqPwm, pinClock, pinData, pinSwitch, fetchLightValue, saveLightValue):

        self.pinPwm = pinPwm
        self.freqPwm = freqPwm
        self.pinClock = pinClock
        self.pinData = pinData
        self.pinSwitch = pinSwitch

        self.fetchLightValue = fetchLightValue
        self.saveLightValue = saveLightValue

        self.saPwm = SAPwm(pinPwm, freqPwm)
        self.saKy040 = SAKy040(pinClock, pinData, pinSwitch, self.rotaryChanged, self.switchPressed)
        self.saPwm.configure()
        self.saKy040.configure()

        self.actuatorLightId = self.__class__.ACTUATOR_LIGHT_ID

    def getActuatorLightId(self):
        return self.actuatorLightId

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

    def unconfigure(self):
        self.saPwm.unconfigure()
        self.saKy040.unconfigure()

