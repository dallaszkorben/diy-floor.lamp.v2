#! /usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from time import time
from threading import Thread

#if __name__ == "__main__":
#from sa import SA
#else:
from senact.sa import SA

class SAKy040(SA):

    INCREASE_SLOW = 1
    INCREASE_FAST = 10

    DECREASE_SLOW = -1
    DECREASE_FAST = -10
    STANDBY = 0

    MIN_DIFF_TIME = 0.1

    def __init__(self, clockPin, dataPin, switchPin, rotaryCallback, switchCallback):

        GPIO.setmode(GPIO.BCM)

        #persist values
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.switchPin = switchPin
        self.rotaryCallback = rotaryCallback
        self.switchCallback = switchCallback

        #setup pins
        GPIO.setup(self.clockPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.dataPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.last_change = 0
        self.last_change_time = time()

    def configure(self):

        GPIO.add_event_detect(self.clockPin,
                              GPIO.FALLING,
                              callback=self._clockFallingCallback,
                              bouncetime=50)

        GPIO.add_event_detect(self.dataPin,
                              GPIO.FALLING,
                              callback=self._dataFallingCallback,
                              bouncetime=50)

        GPIO.add_event_detect(self.switchPin,
                              GPIO.FALLING,
                              callback=self._switchCallback,
                              bouncetime=350)

    def unconfigure(self):
        GPIO.remove_event_detect(self.clockPin)
        GPIO.remove_event_detect(self.dataPin)
        GPIO.remove_event_detect(self.switchPin)
        GPIO.cleanup()


    # control clockwise turn
    def _clockFallingCallback(self, pin):

        if GPIO.input(self.dataPin) == 1:

            current_time = time()
            diff = current_time - self.last_change_time

            change = self.STANDBY

            # if more than 1 sec elapsed since the last change
            if(diff >= self.__class__.MIN_DIFF_TIME):

                # then anything this operation is allowed with normal speed
                change = self.__class__.INCREASE_SLOW

            # if less than 1 sec elapsed since the last change 
            # and the previous direction was clockwise
            elif self.last_change > 0 :

                # then only 
                change = self.__class__.INCREASE_FAST

            if not change == self.STANDBY:
                self.last_change = change
                self.last_change_time = time()
                self.rotaryCallback(change)

        else:
            pass

    # couter clockwise turn
    def _dataFallingCallback(self, pin):

        if GPIO.input(self.clockPin) == 1:

            current_time = time()
            diff = current_time - self.last_change_time

            change = self.STANDBY

            # if more than 1 sec elapsed since the last change
            if(diff >= self.__class__.MIN_DIFF_TIME):

                # then anything this operation is allowed with normal speed
                change = self.__class__.DECREASE_SLOW

            # if less than 1 sec elapsed since the last change 
            # and the previous direction was counter clockwise
            elif self.last_change < 0 :

                # then only 
                change = self.__class__.DECREASE_FAST

            if not change == self.STANDBY:
                self.last_change = change
                self.last_change_time = time()
                self.rotaryCallback(change)

        else:
            pass

    def _switchCallback(self, pin):
        if GPIO.input(self.switchPin) == 0:
            self.switchCallback()

#test
if __name__ == "__main__":

    CLOCK_PIN = 17
    DATA_PIN = 27
    SWITCH_PIN = 23

    def rotaryChange(value):
        print( "turned - ", str(value))

    def switchPressed():
        print ("button pressed")

    ky040 = SAKy040(CLOCK_PIN, DATA_PIN, SWITCH_PIN, rotaryChange, switchPressed)
    ky040.configure()

    try:
        while True:
            sleep(10)
    finally:
        ky040.unconfigure()
