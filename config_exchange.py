import os
import configparser
from pathlib import Path
import logging
from builtins import UnicodeDecodeError

from property import Property

class Config:
    HOME = str(Path.home())
    CONFIG_FOLDER = '.lightcontrol'

    @staticmethod 
    def get_path_to_config_folder():
        return os.path.join(Config.HOME, Config.CONFIG_FOLDER)

class ConfigExchange( Property ):
    INI_FILE_NAME="config_exchange.ini"

    # (section, key, default)
    DEFAULT_ACTUATOR_LIGHT_LEVEL = ("actuator", "light-value", "0")

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
        folder = os.path.join(Config.HOME, Config.CONFIG_FOLDER)
        file = os.path.join(folder, ConfigExchange.INI_FILE_NAME)
        super().__init__( file, True, folder )

    def getLightValue(self):
        return self.get(self.DEFAULT_ACTUATOR_LIGHT_LEVEL[0], self.DEFAULT_ACTUATOR_LIGHT_LEVEL[1], self.DEFAULT_ACTUATOR_LIGHT_LEVEL[2])

# ---

    def setLightValue(self, lightValue):
        self.update(self.DEFAULT_ACTUATOR_LIGHT_LEVEL[0], self.DEFAULT_ACTUATOR_LIGHT_LEVEL[1], lightValue)

# ---
# ---

def getConfigExchange():
    return ConfigExchange.getInstance()

def getConfig():
    ce = getConfigExchange()
    config = {}

    config['light-value'] = ce.getLightValue()

    return config

def setConfig(config):
    ce = getConfigExchange()

    if "light-value" in config:
        ce.setLightValue(config["light-value"])

