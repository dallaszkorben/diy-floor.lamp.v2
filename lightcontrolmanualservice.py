#! /usr/bin/python3

import RPi.GPIO as GPIO

import pigpio
from time import sleep

from converter import Converter
from iob_ky040 import IOBKy040

PIN_PWM = 18 #12 #18
#PIN_UP = 23 #16 #23
#PIN_DOWN = 24 #18 #24

PWM_FREQ = 800

MIN_DUTY_CYCLE = 0
MAX_DUTY_CYCLE = 1000000

SLEEP = 5

POTMETER_MIN = 0.0
POTMETER_MAX = 100.0
POTMETER_STEP = 1.0

actuators = {
    '1':{'pin': PIN_PWM, 'freq': PWM_FREQ, 'min-duty-cycle': MIN_DUTY_CYCLE, 'max-duty-cycle': MAX_DUTY_CYCLE}
}
#sensors = {
#    'up':{'pin': PIN_UP}, 
#    'down':{'pin': PIN_DOWN}
#}

class Board(object):
    __instance = None

    @classmethod
    def getInstance(cls):
        inst = cls.__new__(cls)
        cls.__init__(cls.__instance) 
        return inst

    def __new__(cls):
        if Board.__instance is None:
            Board.__instance = object.__new__(cls)
        return Board.__instance

    def __init__(self):

        self.pi_pwm = pigpio.pi()

        self.pi_pwm.set_mode(PIN_PWM, pigpio.OUTPUT)
#        self.pi_pwm.set_mode(PIN_UP, pigpio.INPUT)
#        self.pi_pwm.set_mode(PIN_DOWN, pigpio.INPUT)

    def setPwmByValue(self, actuator, value):

        # calculate the pwm by value
        fadeValue = Converter.getLinearValueToExponential(value, POTMETER_MAX, MAX_DUTY_CYCLE)

        # Change the Duty Cycle
        self.pi_pwm.hardware_PWM(actuators[actuator]['pin'], actuators[actuator]['freq'], fadeValue)

        return fadeValue

#    def getSensorUp(self):
#        return self.pi_pwm.read(sensors['up']['pin'])
#
#    def getSensorDown(self):
#        return self.pi_pwm.read(sensors['down']['pin'])


board = Board.getInstance()

# 0-100
potmeterValue = POTMETER_MIN

actuatorLight = '1'

def rotaryChange(value):
    global potmeterValue
    global actuatorLight
    global board
    potmeterValue += value

    if potmeterValue > POTMETER_MAX:
        potmeterValue = POTMETER_MAX
    elif potmeterValue < POTMETER_MIN:
        potmeterValue = POTMETER_MIN

    print( "turned - ", str(potmeterValue))
    pwmValue = board.setPwmByValue(actuatorLight, potmeterValue)


def switchPressed():
    global potmeterValue
    global actuatorLight
    global board
    print ("button pressed")
    if potmeterValue:
        potmeterValue  = POTMETER_MIN
    else:
        potmeterValue =  POTMETER_MAX
    pwmValue = board.setPwmByValue(actuatorLight, potmeterValue)

CLOCK_PIN = 17
DATA_PIN = 27
SWITCH_PIN = 23

ky040 = IOBKy040(CLOCK_PIN, DATA_PIN, SWITCH_PIN, rotaryChange, switchPressed)
ky040.configure()

try:
    while True:
        sleep(SLEEP)
finally:
    ky040.unconfigure()
#    GPIO.cleanup()
