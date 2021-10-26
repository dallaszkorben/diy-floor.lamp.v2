from machine import Pin, PWM, Signal
import time
from rotary_irq_esp import RotaryIRQ
import math

LED_OUT_GPIO=2

pin = Pin(LED_OUT_GPIO, Pin.OUT)
#signal = Signal(LED_OUT_GPIO, Pin.OUT, invert=True)
pwm0 = PWM(Pin(LED_OUT_GPIO))	# create PWM object from a pin
pwm0.freq(100)			# set frequency
pwm0.duty(0)			# set duty cycle

r = RotaryIRQ(pin_num_clk=4,
              pin_num_dt=0,
              min_val=0,
              max_val=33,
              reverse=True,
              range_mode=RotaryIRQ.RANGE_BOUNDED
#              range_mode=RotaryIRQ.RANGE_UNBOUNDED
#              range_mode=RotaryIRQ.RANGE_WRAP
)



def start():
    val_old = r.value()

    while True:
        val_new = r.value()

        if val_old != val_new:
            val_old = val_new

            val_to_show =  val_new if val_new < 10 else val_new*val_new - 90

            print('result =', val_to_show, val_new)
            pwm0.duty(int(val_to_show))

        time.sleep_ms(50)

start()