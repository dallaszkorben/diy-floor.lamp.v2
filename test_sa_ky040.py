#! /usr/bin/python3

from senact.sa_ky040 import SAKy040
from time import sleep

if __name__ == "__main__":

    CLOCK_PIN = 17
    DATA_PIN = 27
    SWITCH_PIN = 23

    def rotaryChange(value):
        print( "turned - ", str(value))

    def switchPressed():
        print ("button pressed")

    ky040 = SAKy040("1", CLOCK_PIN, DATA_PIN, SWITCH_PIN, rotaryChange, switchPressed)
    ky040.configure()

    try:
        while True:
            sleep(10)
    finally:
        ky040.unconfigure()
