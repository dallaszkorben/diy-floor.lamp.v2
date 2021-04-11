# diy-floor.lamp.v2

Floor lamp dimmable manually and/or through web service. It is based on "diy-floor.lamp" project: https://github.com/dallaszkorben/diy-floor.lamp

There are 3 version of the ad the SW

- Raspberry PI Zero W
- Arduiono Nano
- ESP2866 NodeMCU

All verson uses the same 3D printouts and other accessories.


## Raspberry PI Zero W

Python dependencies: pip3 install git+https://github.com/teracyhq/flask-classful.git@develop#egg-flask-classful Not pip3 install flask-classful because we need version=0.15.0, otherwise ConfigView.register(self.app, init_argument=self) can't be use because init_argument attribute does not work pip3 install flask pip3 install flask-cors pip3 install tzlocal


Before you run start.py the pigpiod should run as we us pigpio library

Python dependencies:
 - pip3 install git+https://github.com/teracyhq/flask-classful.git@develop#egg-flask-classful
        Not pip3 install flask-classful because we need version=0.15.0, otherwise ConfigView.register(self.app, init_argument=self) can't be use because init_argument attribute does not work
 - pip3 install flask
 - pip3 install flask-cors
 - pip3 install tzlocal

Other dependencies:
 - sudo apt install apache2 -y
 - npm install jquery

