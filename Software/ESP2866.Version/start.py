from machine import Pin, PWM
import time
from rotary_irq_esp import RotaryIRQ


pwm0 = PWM(Pin(0))		# create PWM object from a pin
pwm0.freq(100)			# set frequency
pwm0.duty(0)			# set duty cycle

r = RotaryIRQ(pin_num_clk=13,
              pin_num_dt=12,
              min_val=0,
              max_val=100,
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
            print('result =', val_new)
            pwm0.duty(val_new)

        time.sleep_ms(50)

start()