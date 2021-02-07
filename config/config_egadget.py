import os
import configparser
from pathlib import Path
import logging

from config.property import Property
from config.config_location import ConfigLocation

class ConfigEGadget( Property ):
    INI_FILE_NAME="config_egadget.ini"

    # (section, key, default)
    DEFAULT_ACTUATOR_1_PWM_PIN = ("actuator-1", "pin", 18)
    DEFAULT_ACTUATOR_1_PWM_FREQ = ("actuator-1", "freq", 800)
    DEFAULT_ACTUATOR_1_PWM_MIN_DUTY_CYCLE = ("actuator-1", "min-duty-cycle", 0)
    DEFAULT_ACTUATOR_1_PWM_MAX_DUTY_CYCLE = ("actuator-1", "max-duty-cycle", 1000000)

    DEFAULT_SENSOR_UP_PIN = ("sensor-up", "pin", "23")

    DEFAULT_SENSOR_DOWN_PIN = ("sensor-down", "pin", "24")

    DEFAULT_POTMETER_MIN = ("potmeter", "min", "0")
    DEFAULT_POTMETER_MAX = ("potmeter", "max", "100")
    DEFAULT_POTMETER_STEP = ("potmeter", "step", "1")

    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        inst = cls.__new__(cls)
        cls.__init__(cls.__instance)
        return inst

# ---

    def __init__(self):
        folder = os.path.join(ConfigLocation.HOME, ConfigLocation.CONFIG_FOLDER)
        file = os.path.join(folder, ConfigEGadget.INI_FILE_NAME)
        super().__init__( file, True, folder )

    def getActuator1PwmPin(self):
        return self.get(self.DEFAULT_ACTUATOR_1_PWM_PIN[0], self.DEFAULT_ACTUATOR_1_PWM_PIN[1], self.DEFAULT_ACTUATOR_1_PWM_PIN[2])

    def getActuator1PwmFreq(self):
        return self.get(self.DEFAULT_ACTUATOR_1_PWM_FREQ[0], self.DEFAULT_ACTUATOR_1_PWM_FREQ[1], self.DEFAULT_ACTUATOR_1_PWM_FREQ[2])

    def getActuator1PwmMinDutyCycle(self):
        return self.get(self.DEFAULT_ACTUATOR_1_PWM_MIN_DUTY_CYCLE[0], self.DEFAULT_ACTUATOR_1_PWM_MIN_DUTY_CYCLE[1], self.DEFAULT_ACTUATOR_1_PWM_MIN_DUTY_CYCLE[2])

    def getActuator1PwmMaxDutyCycle(self):
        return self.get(self.DEFAULT_ACTUATOR_1_PWM_MAX_DUTY_CYCLE[0], self.DEFAULT_ACTUATOR_1_PWM_MAX_DUTY_CYCLE[1], self.DEFAULT_ACTUATOR_1_PWM_MAX_DUTY_CYCLE[2])

    def getSensorUpPin(self):
        return self.get(self.DEFAULT_SENSOR_UP_PIN[0], self.DEFAULT_SENSOR_UP_PIN[1], self.DEFAULT_SENSOR_UP_PIN[2])

    def getSensorDownPin(self):
        return self.get(self.DEFAULT_SENSOR_DOWN_PIN[0], self.DEFAULT_SENSOR_DOWN_PIN[1], self.DEFAULT_SENSOR_DOWN_PIN[2])

    def getPotmeterMin(self):
        return self.get(self.DEFAULT_POTMETER_MIN[0], self.DEFAULT_POTMETER_MIN[1], self.DEFAULT_POTMETER_MIN[2])

    def getPotmeterMax(self):
        return self.get(self.DEFAULT_POTMETER_MAX[0], self.DEFAULT_POTMETER_MAX[1], self.DEFAULT_POTMETER_MAX[2])

    def getPotmeterStep(self):
        return self.get(self.DEFAULT_POTMETER_STEP[0], self.DEFAULT_POTMETER_MAX[1], self.DEFAULT_POTMETER_STEP[2])

# ---

    def setLightValue(self, lightValue):
        self.update(self.DEFAULT_ACTUATOR_LIGHT_LEVEL[0], self.DEFAULT_ACTUATOR_LIGHT_LEVEL[1], lightValue)

    def setActuator1PwmPin(self, pin):
        self.update(self.DEFAULT_ACTUATOR_1_PWM_PIN[0], self.DEFAULT_ACTUATOR_1_PWM_PIN[1], pin)

    def setActuator1PwmFreq(self, freq):
        self.update(self.DEFAULT_ACTUATOR_1_PWM_FREQ[0], self.DEFAULT_ACTUATOR_1_PWM_FREQ[1], freq)

    def setActuator1PwmMinDutyCycle(self, minDutyCycle):
        self.update(self.DEFAULT_ACTUATOR_1_PWM_MIN_DUTY_CYCLE[0], self.DEFAULT_ACTUATOR_1_PWM_MIN_DUTY_CYCLE[1], minDutyCycle)

    def setActuator1PwmMaxDutyCycle(self, maxDutyCycle):
        self.update(self.DEFAULT_ACTUATOR_1_PWM_MAX_DUTY_CYCLE[0], self.DEFAULT_ACTUATOR_1_PWM_MAX_DUTY_CYCLE[1], maxDutyCycle)

    def setSensorUpPin(self, pin):
        self.update(self.DEFAULT_SENSOR_UP_PIN[0], self.DEFAULT_SENSOR_UP_PIN[1], pin)

    def setSensorDownPin(self, pin):
        self.update(self.DEFAULT_SENSOR_DOWN_PIN[0], self.DEFAULT_SENSOR_DOWN_PIN[1], pin)

    def setPotmeterMin(self, min):
        self.update(self.DEFAULT_POTMETER_MIN[0], self.DEFAULT_POTMETER_MIN[1], min)

    def setPotmeterMax(self, max):
        self.update(self.DEFAULT_POTMETER_MAX[0], self.DEFAULT_POTMETER_MAX[1], max)

    def setPotmeterStep(self, step):
        self.update(self.DEFAULT_POTMETER_STEP[0], self.DEFAULT_POTMETER_MAX[1], step)

# ---
# ---

def getConfigEGadget():
    cb = ConfigEGadget.getInstance()
    config = {}

    config["actuator-1-pin"] = cb.getActuator1PwmPin()
    config["actuator-1-freq"] = cb.getActuator1PwmFreq()
    config["actuator-1-min-duty-cycle"] = cb.getActuator1PwmMinDutyCycle()
    config["actuator-1-max-duty-cycle"] = cb.getActuator1PwmMaxDutyCycle()

    config["sensor-up-pin"] = cb.getSensorUpPin()

    config["sensor-down-pin"] = cb.getSensorDownPin()

    config["potmeter-min"] = cb.getPotmeterMin()
    config["potmeter-max"] = cb.getPotmeterMax()
    config["potmeter-step"] = cb.getPotmeterStep()

    return config

def setConfigEGadget(config):
    cb = ConfigEGadget.getInstance()

    if "actuator-1-pin" in config:
        cb.setActuator1PwmPin(config["actuator-1-pin"])

    if "actuator-1-freq" in config:
        cb.setActuator1PwmFreq(config["actuator-1-freq"])

    if "actuator-1-min-duty-cycle" in config:
        cb.setActuator1PwmMinDutyCycle(config["actuator-1-min-duty-cycle"])

    if "actuator-1-max-duty-cycle" in config:
         cb.setActuator1PwmMaxDutyCycle(config["actuator-1-max-duty-cycle"])

    if "sensor-up-pin" in config:
         cb.setSensorUpPin(config["sensor-up-pin"])

    if "sensor-down-pin" in config:
         cb.setSensorDownPin()

    if "potmeter-min" in config:
         cb.setPotmeterMin(config["potmeter-min"])

    if "potmeter-max" in config:
         cb.setPotmeterMax(config["potmeter-max"])

    if "potmeter-step" in config:
         cb.setPotmeterStep(config["potmeter-step"])

