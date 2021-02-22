#! /usr/bin/python3

from wgadget.wg_light import WGLight

if __name__ == "__main__":

#    PIN_PWM = 18
#    FREQ_PWM = 800

#    PIN_CLOCK = 17
#    PIN_DATA = 27
#    PIN_SWITCH = 23

#    GADGET_NAME = "Light"
#    ACTUATOR_LIGHT_ID = 1
#    SENSOR_POTMETER_ID = 1

#    wgLight = WGLight( GADGET_NAME, ACTUATOR_LIGHT_ID, PIN_PWM, FREQ_PWM, SENSOR_POTMETER_ID, PIN_CLOCK, PIN_DATA, PIN_SWITCH )
    wgLight = WGLight()

    try:
        wgLight.run(host= '0.0.0.0')
    finally:
        wgLight.unconfigure()
