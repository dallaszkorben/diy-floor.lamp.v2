#! /usr/bin/python3

import json
from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from representations import output_json

from threading import Thread

from senact.sa_light import SALight

from config_exchange import getConfigExchange
from config_exchange import setConfigExchange
from config_board import getConfigBoard

class EGLight(object):

    # ---------------------------------
    #
    # GET Configuration Information
    #
    # ---------------------------------
    # GET http://localhost:5000/config
    class ConfigView(FlaskView):
        representations = {'application/json': output_json}

        def __init__(self, parent):
            self.parent = parent

        #
        # GET http://localhost:5000/config/
        #
        def index(self):
            return self.getConfig()

        #
        # GET http://localhost:5000/config
        #
        @route("",  methods=['GET'] )
        def getConfig(self):

            lightValue = self.parent.fetchLightValue()
            json_data = {
                          'actuators': [
                            {
                              'id': '1',
                              'name': 'lamp',
                              'type': 'integer',
                              'min': 0,
                              'max': 100,
                              'actual': lightValue
                            }
                          ],
                          'sensors': [
                          ]
                        }
            return json_data

    # ---

    # ---------------------------------
    #
    # POST Contorl the level of the light
    #
    # ---------------------------------
    #
    # GET http://localhost:5000/actuator
    class ActuatorView(FlaskView):
        representations = {'application/json': output_json}
        inspect_args = False

        def __init__(self, parent):
            self.parent = parent

        #
        # GET http://localhost:5000/actuator/
        #
        def index(self):
            print('hello')
            return {}

        #
        # Simple way to set the light value
        #
        # POST http://localhost:5000/acturator/1/value/13
        #
        @route('/<id>/value/<value>', methods=['POST'])
        def post(self, id, value):

            try:
                actuatorId = int(id)
                value = int(value)
            except(ValueError):
                actuatorId = -1
            if actuatorId == 1:

                if value >= 0 and value <= 100:

                    # Save the light value and set the Light
                    self.parent.setLight(value)

                    print("                                      POST /actuator", "id=", id, "value=", value)

                else:
                    raise InvalidAPIUsage("The value is not valid: {0}".format(value), status_code=404)

            else:
                raise InvalidAPIUsage("No such actuator: {0} or value: {1}".format(id, value), status_code=404)

            return {'status': 'OK'}

        #
        # Alternative way to set the light value using the body
        #
        # POST http://localhost:5000/acturator
        #      body: {
        #                'id': "1',
        #                'value: '13'
        #           }
        #
        @route("",  methods=['POST'] )
        def postActuator(self):

            if request.form:

                if 'id' in request.form:
                    print('id', request.form['id'])
                if 'value' in request.form:
                    print('value', request.form['value'])

                id = request.form['id']
                value = request.form['value']

            elif request.json:

                json_data = request.json
                id = json_data["id"]
                value = json_data["value"]

            else:
                return 

            print(id, value)
            return self.post(id, value)

        #
        # Simple way to increase/decrease the light value gradually
        #
        # POST http://localhost:5000/acturator/1/stepvalue/-10
        #
        @route('/<id>/stepvalue/<step_value>/inseconds/<in_seconds>', methods=['POST'])
        def postActuatorStepValueGradually(self, id, step_value, in_seconds):

            try:
                actuatorId = int(id)
                stepValue = int(step_value)
                inSeconds = int(in_seconds)
            except(ValueError):
                actuatorId = -1
            if actuatorId == 1:

                actual_value = self.parent.fetchLightValue()

                try:
                    actualValue = int(actual_value)
                except(ValueError):
                    actualValue = 0

                newValue = actualValue + stepValue
                if newValue < self.parent.POTMETER_MIN:
                    newValue = self.parent.POTMETER_MIN

                elif newValue > self.parent.POTMETER_MAX:
                    newValue = self.parent.POTMETER_MAX

                thread = Thread(target = self.parent.setLightGradually, args = (id, actualValue, newValue, inSeconds)) 
                thread.daemon = True
                thread.start()

                print("                                      POST /actuator", "id=", id, "startValue=", actualValue, "stepValue=", stepValue, "newValue=", newValue)

            else:

                raise InvalidAPIUsage("No such actuator: {0} or step value: {1} or seconds {2}".format(id, step_value, in_seconds), status_code=404)

            return {'status': 'OK'}


# ---

    def __init__(self, pinPwm, freqPwm, pinClock, pinData, pinSwitch):

        cb = getConfigBoard()
        try:
            self.POTMETER_MIN = int(cb["potmeter-min"])
        except(ValueError):
            self.POTMETER_MIN = 0
        try:
            self.POTMETER_MAX = int(cb["potmeter-max"])
        except(ValueError):
            self.POTMETER_MAX = 100
        try:
            self.POTMETER_STEP = cb["potmeter-min"]
        except(ValueError):
            self.POTMETER_STEP = 1

        self.saLight = SALight( pinPwm, freqPwm, pinClock, pinData, pinSwitch, self.fetchLightValue, self.saveLightValue )
        self.actuatorLightId = self.saLight.getActuatorLightId()

        self.app = Flask(__name__)

        # register the end-points
        self.ConfigView.register(self.app, init_argument=self)
        self.ActuatorView.register(self.app, init_argument=self)

    def unconfigure(self):
        self.saLight.unconfigure()

    def run(self, host='0.0.0.0'):
        self.app.run(host=host)

    def setLight(self, value):
        self.saLight.setLight(value)

    def setLightGradually(self, actuator, fromValue, toValue, inSeconds):
        self.saLight.setLightGradually(actuator, fromValue, toValue, inSeconds)

    def fetchLightValue(self):
        config_ini = getConfigExchange()
        return int(config_ini["light-value"])

    def saveLightValue(self, value):
        config_ini = getConfigExchange()
        config_ini["light-value"] = value
        setConfigExchange(config_ini)

if __name__ == "__main__":

    PIN_PWM = 18
    FREQ_PWM = 800

    PIN_CLOCK = 17
    PIN_DATA = 27
    PIN_SWITCH = 23

    egLight = EGLight( PIN_PWM, FREQ_PWM, PIN_CLOCK, PIN_DATA, PIN_SWITCH )

    try:
        egLight.run(host= '0.0.0.0')
    finally:
        egLight.unconfigure()
