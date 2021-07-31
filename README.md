# diy-floor.lamp.v2

Floor lamp dimmable manually and/or through web service. It is based on "diy-floor.lamp" project: https://github.com/dallaszkorben/diy-floor.lamp

There are 3 version of the HW the SW

- Raspberry PI Zero W
- Arduiono Nano
- ESP2866 NodeMCU

All verson uses the same 3D printouts and other accessories.

## Raspberry PI Zero W

Before you run start.py the pigpiod should run as we use pigpio library

Python dependencies:
 - pip3 install git+https://github.com/teracyhq/flask-classful.git@develop#egg-flask-classful
        Not pip3 install flask-classful because we need version=0.15.0, otherwise ConfigView.register(self.app, init_argument=self) can't be use because init_argument attribute does not work
 - pip3 install flask
 - pip3 install flask-cors
 - pip3 install tzlocal

Other dependencies:
 - sudo apt-get install libapache2-mod-wsgi-py3
 - sudo apt install apache2 -y
 - npm install jquery

