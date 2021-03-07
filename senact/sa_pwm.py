#! /usr/bin/python3

import RPi.GPIO as GPIO

import pigpio
from time import sleep

from threading import Lock

#if __name__ == "__main__":
from senact.sa import SA
import os
import sys

from senact.senact import SenAct

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from converter import Converter

import logging

class SAPwm(SA):

    MIN_VALUE = 0
    MAX_VALUE = 100
    MIN_DUTY_CYCLE = 0
    MAX_DUTY_CYCLE = 1000000

    SENACT_TYPE = SenAct.ACTUATOR

    def __init__(self, id, pwmPin, pwmFreq):

        self.id = id
        self.maxDutyCycle = self.__class__.MAX_DUTY_CYCLE
        self.maxValue = self.__class__.MAX_VALUE

        self.pwmPin = pwmPin
        self.pwmFreq = pwmFreq

        self.pi_pwm = pigpio.pi()
        self.pi_pwm.set_mode(self.pwmPin, pigpio.OUTPUT)

        self.lock = Lock()

    def getSenactType(self):
        return self.__class__.SENACT_TYPE

    def getSenactId(self):
        return self.id

    def setPwmByValue(self, value):

        # sychronizing the method
        with self.lock:

            # calculate the pwm by value
            fadeValue = Converter.getLinearValueToExponential(value, self.maxValue, self.maxDutyCycle)

            # Change the Duty Cycle
            self.pi_pwm.hardware_PWM(self.pwmPin, self.pwmFreq, fadeValue)

            logging.debug( "Set PWM Duty Cycle to {0} (input: {1}) in {2} Hz frequency on PIN #{3} --- FILE: {4}".format(
                fadeValue,
                value,
                self.pwmFreq,
                self.pwmPin,
                __file__)
            )


        return fadeValue

    def setPwmByStepValueGradually(self, actuator, fromValue, toValue, inSeconds):

        diff = toValue - fromValue

        if diff == 0:
            logging.debug("PWM Duty Cycle did not change as the value {0} (input: {1}) was already set --- FILE: {2}".format(
                Converter.getLinearValueToExponential(toValue, self.maxValue, self.maxDutyCycle),
                toValue,
                __file__)
            )
            return

        with self.lock:

            secInOneStep = abs(inSeconds / diff)

            if diff >= 0:
                par1 = fromValue
                par2 = toValue + 1
                par3 = 1

            elif diff < 0:
                par1 = fromValue
                par2 = toValue - 1
                par3 = -1

            logging.debug("Set PWM Duty Cycle gradually from {0} (input: {1}) to {2} (<-{3}) in {4} seconds --- FILE: {5}".format(
                Converter.getLinearValueToExponential(fromValue, self.maxValue, self.maxDutyCycle),
                fromValue,
                Converter.getLinearValueToExponential(toValue, self.maxValue, self.maxDutyCycle),
                toValue,
                inSeconds,
                __file__)
            )

            for value in range(par1, par2, par3):
                #print("waiting:", secInOneStep, "value: ", value)
                sleep(secInOneStep)

                fadeValue = Converter.getLinearValueToExponential(value, self.maxValue, self.maxDutyCycle)
                self.pi_pwm.hardware_PWM(self.pwmPin, self.pwmFreq, fadeValue)

                logging.debug( "    Set to {0} (input: {1}) in {2} frequency on PIN #{3} --- FILE: {4}".format(
                    fadeValue,
                    value,
                    self.pwmFreq,
                    self.pwmPin,
                    __file__)
                )

            logging.debug("Set PWM Duty Cycle gradually is done")

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



