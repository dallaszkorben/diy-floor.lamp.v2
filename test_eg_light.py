#! /usr/bin/python3

from egadget.eg_light import EGLight
from time import sleep

if __name__ == "__main__":

    PIN_PWM = 18
    FREQ_PWM = 800

    PIN_CLOCK = 17
    PIN_DATA = 27
    PIN_SWITCH = 23

    potmeterValue = 0

    def getPotmeterValue():
        global potmeterValue
        return potmeterValue

    def setPotmeterValue(value):
        global potmeterValue
        potmeterValue = value;

    saLight = EGLight( "Lamp", "1", PIN_PWM, FREQ_PWM, "1", PIN_CLOCK, PIN_DATA, PIN_SWITCH, getPotmeterValue, setPotmeterValue )

    try:
        while True:
            sleep(10)
    finally:
        saLight.unconfigure()