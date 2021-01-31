import os
import configparser
from pathlib import Path
import logging

class ConfigLocation:
    HOME = str(Path.home())
    CONFIG_FOLDER = '.lightcontrol'

    @staticmethod 
    def get_path_to_config_folder():
        return os.path.join(Config.HOME, Config.CONFIG_FOLDER)
