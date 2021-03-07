#! /usr/bin/python3

import os
from time import sleep
from senact.sa_ky040 import SAKy040
from senact.sa_pwm import SAPwm
from egadget.eg_light import EGLight

import logging
from logging.handlers import RotatingFileHandler


#test
if __name__ == "__main__":

    SENSOR_ID = 1

    CLOCK_PIN = 17
    DATA_PIN = 27
    SWITCH_PIN = 23

    ACTUATOR_ID = 1

    PWM_PIN = 18
    PWM_FREQ = 800

    DIR_UP = 1
    DIR_DOWN = -1

    def switchCallback():

        lightValue = egLight.lightValue

        print(lightValue)

        if lightValue['current'] > egLight.minLightValue:
            fromValue = lightValue['current']
            toValue = egLight.minLightValue
            turned = "off"

        else:
            fromValue = egLight.minLightValue

            if lightValue['current'] == lightValue['previous']:
                toValue = egLight.maxLightValue
            else:
                toValue = lightValue['previous']
            turned = "on"

        print("Switch started")
        result = egLight.setLightGradually(ACTUATOR_ID, fromValue, toValue, 3)
        print(result)

        return result

    def rotaryCallback(value):

        result = egLight.rotaryCallbackMethod(value)
        print(result)

        return result

    # LOG 
    logPath = os.path.join(".", "test.log")
    logLevel = "INFO" #"DEBUG"
    logging.basicConfig(
        handlers=[RotatingFileHandler(logPath, maxBytes=5*1024*1024, backupCount=5)],
        format='%(asctime)s %(levelname)8s - %(message)s' , 
        level = logging.ERROR if logLevel == 'ERROR' else logging.WARNING if logLevel == 'WARNING' else logging.INFO if logLevel == 'INFO' else logging.DEBUG if logLevel == 'DEBUG' else 'CRITICAL' )


    saPwm = SAPwm(ACTUATOR_ID, PWM_PIN, PWM_FREQ)
    saKy040 = SAKy040(SENSOR_ID, CLOCK_PIN, DATA_PIN, SWITCH_PIN)

    egLight = EGLight( "Light", saPwm, saKy040, fetchSavedLightValue=None, saveLightValue=None, switchCallbackMethod=switchCallback, rotaryCallbackMethod=rotaryCallback )

    print(egLight.getGadgetName(), 'has started')

    try:
        while True:
            sleep(10)
    finally:
        egLight.unconfigure()








