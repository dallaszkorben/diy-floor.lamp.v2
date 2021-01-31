import pigpio

from converter import Converter

from config_board import getConfigBoard
from config_board import setConfigBoard

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

        cb = getConfigBoard()

        ACTUATOR_1_PIN_PWM = cb["actuator-1-pin"]
        ACTUATOR_1_PWM_FREQ = cb["actuator-1-freq"]

        ACTUATOR_1_MIN_DUTY_CYCLE = cb["actuator-1-min-duty-cycle"]
        ACTUATOR_1_MAX_DUTY_CYCLE = cb["actuator-1-max-duty-cycle"]

        SENSOR_UP_PIN = cb["sensor-up-pin"]
        SENSOR_DOWN_PIN = cb["sensor-down-pin"]

        #POTMETER_MIN = cb["potmeter-min"]
        POTMETER_MAX = cb["potmeter-max"]
        #POTMETER_STEP = cb["potmeter-min"]

        self.potmeterMax = POTMETER_MAX

        self.actuators = {
            '1':{'pin': ACTUATOR_1_PIN_PWM, 'freq': ACTUATOR_1_PWM_FREQ, 'min-duty-cycle': ACTUATOR_1_MIN_DUTY_CYCLE, 'max-duty-cycle': ACTUATOR_1_MAX_DUTY_CYCLE}
        }
        self.sensors = {
            'up':{'pin': SENSOR_UP_PIN}, 
            'down':{'pin': SENSOR_DOWN_PIN}
        }

        self.pi_pwm = pigpio.pi()

        self.pi_pwm.set_mode(int(self.actuators['1']['pin']), pigpio.OUTPUT)
        self.pi_pwm.set_mode(int(self.sensors['up']['pin']), pigpio.INPUT)
        self.pi_pwm.set_mode(int(self.sensors['down']['pin']), pigpio.INPUT)

    def setPwmByValue(self, actuator, value):

        # calculate the pwm by value
        fadeValue = Converter.getLinearValueToExponential(value, int(self.potmeterMax), int(self.actuators[actuator]['max-duty-cycle']))

        # Change the Duty Cycle
        self.pi_pwm.hardware_PWM(int(self.actuators[actuator]['pin']), int(self.actuators[actuator]['freq']), fadeValue)

        return fadeValue

    def getSensorUp(self):
        return self.pi_pwm.read(self.sensors['up']['pin'])

    def getSensorDown(self):
        return self.pi_pwm.read(self.sensors['down']['pin'])


#board = Board.getInstance()
