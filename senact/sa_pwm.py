#! /usr/bin/python3

import RPi.GPIO as GPIO

import pigpio
from time import sleep

#if __name__ == "__main__":
from senact.sa import SA
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from converter import Converter

#else:
#    from senact.sa import SA
#    from converter import Converter


#actuators = {
#    '1':{'pin': PIN_PWM, 'freq': PWM_FREQ, 'min-duty-cycle': MIN_DUTY_CYCLE, 'max-duty-cycle': MAX_DUTY_CYCLE}
#}

class SAPwm(SA):

    MIN_VALUE = 0
    MAX_VALUE = 100
    MIN_DUTY_CYCLE = 0
    MAX_DUTY_CYCLE = 1000000


    def __init__(self, pwmPin, pwmFreq):

        self.maxDutyCycle = self.__class__.MAX_DUTY_CYCLE
        self.maxValue = self.__class__.MAX_VALUE

        self.pwmPin = pwmPin
        self.pwmFreq = pwmFreq

        self.pi_pwm = pigpio.pi()
        self.pi_pwm.set_mode(self.pwmPin, pigpio.OUTPUT)

    def setPwmByValue(self, value):

        # calculate the pwm by value
        fadeValue = Converter.getLinearValueToExponential(value, self.maxValue, self.maxDutyCycle)

        # Change the Duty Cycle
        self.pi_pwm.hardware_PWM(self.pwmPin, self.pwmFreq, fadeValue)

        return fadeValue

    def setPwmByStepValueGradually(self, actuator, fromValue, toValue, inSeconds):

        diff = toValue - fromValue
        secInOneStep = abs(inSeconds / diff)

        print("fromValue:", fromValue, "toValue:", toValue, "inSeconds:", inSeconds)

        if diff >= 0:
            par1 = fromValue
            par2 = toValue + 1
            par3 = 1

        elif diff < 0:
            par1 = fromValue
            par2 = toValue - 1
            par3 = -1

        print("par1:", par1, "par2:", par2, "par3:", par3)

        for value in range(par1, par2, par3):
            print("waiting:", secInOneStep, "value: ", value)
            sleep(secInOneStep)

            fadeValue = Converter.getLinearValueToExponential(value, self.maxValue, self.maxDutyCycle)
            self.pi_pwm.hardware_PWM(self.pwmPin, self.pwmFreq, fadeValue)

        print("done  value:", toValue)

        return

    def configure(self):
        pass

    def unconfigure(self):
        pass


#test
if __name__ == "__main__":

    PWM_PIN = 18
    PWM_FREQ = 800

    DIR_UP = 1
    DIR_DOWN = -1

    saPwm = SAPwm(PWM_PIN, PWM_FREQ)
    saPwm.configure()

    def triggerValue(value):
        print(value)
        saPwm.setPwmByValue(1, value)

    try:

        value = 0
        direction = DIR_UP
        while True:

            triggerValue(value)
            value += direction
            if value >= 100:
                direction = DIR_DOWN
            elif value <= 0:
                direction = DIR_UP
            sleep(0.2)

    finally:
        saPwm.unconfigure()
#        GPIO.cleanup()



