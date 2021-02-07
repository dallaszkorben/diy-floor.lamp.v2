#! /usr/bin/python3

import json
from flask import Flask
from flask import jsonify
from flask_classful import FlaskView, route, request
from representations import output_json

from config_exchange import getConfigExchange
from config_exchange import setConfigExchange
from config_board import getConfigBoard

from threading import Thread

from converter import Converter

from board import Board

app = Flask(__name__)

cb = getConfigBoard()
try:
    POTMETER_MIN = int(cb["potmeter-min"])
except(ValueError):
    POTMETER_MIN = 0
try:
    POTMETER_MAX = int(cb["potmeter-max"])
except(ValueError):
    POTMETER_MAX = 100
try:
    POTMETER_STEP = cb["potmeter-min"]
except(ValueError):
    POTMETER_STEP = 1

class ServiceControl:

#    def __init__(self):

    class InvalidAPIUsage(Exception):
        def __init__(self, message, status_code=None, payload=None):
            super().__init__(message)
            if status_code is not None:
                self.code = status_code
            else:
                self.code = 400
            self.payload = payload

    # ---------------------------------
    #
    # GET Configuration Information
    #
    # ---------------------------------
    # GET http://localhost:5000/config
    class ConfigView(FlaskView):
        representations = {'application/json': output_json}

        def __init__(self, message):
            print(message)

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
            config_ini = getConfigExchange()
            lightValue = config_ini["light-value"]
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

    # ---------------------------------
    #
    # GET Template Information for set
    #
    # ---------------------------------
    # GET http://localhost:5000/config
    class TemplateView(FlaskView):
        representations = {'application/json': output_json}

        #
        # GET http://localhost:5000/template/
        #
        def index(self):
            return {}

        #
        # GET http://localhost:5000/template/actuator/1
        #
        @route("/actuator/<id>",  methods=['GET'] )
        def get(self, id):
            config_ini = getConfigExchange()
            #lightValue = config_ini["light-value"]
            try:
                actuatorId = int(id)
            except(ValueError):
                actuatorId = -1
            if actuatorId == 1:
                json_data = {
                              'id': '1',
                              'value': '{{light_value}}'
                            }
            else:
                json_data = {}
            return json_data


    # ---------------------------------
    #
    # POST Contorl the level of the light
    #
    # ---------------------------------
    # GET http://localhost:5000/config
    # GET http://localhost:5000/config
    class ActuatorView(FlaskView):
        representations = {'application/json': output_json}
        inspect_args = False

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

                    config_ini = getConfigExchange()
                    config_ini["light-value"] = value
                    setConfigExchange(config_ini)

                    Board.getInstance().setPwmByValue(id, value)

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




            #json_data = request.get_json(force=True) 
#            print('json_data', json_data)
#            json_data = request.json





            print(id, value)
            return self.post(id, value)

#stepvalue
#inseconds



# ---

        #
        # Simple way to increase/decrease the light value unneduately
        #
        # POST http://localhost:5000/acturator/1/stepvalue/-10
        #
        @route('/<id>/stepvalue/<step_value>', methods=['POST'])
        def postActuatorStepValueImmediately(self, id, step_value):

            try:
                actuatorId = int(id)
                stepValue = int(step_value)
            except(ValueError):
                actuatorId = -1
            if actuatorId == 1:

#
                config_ini = getConfigExchange()
                actual_value = config_ini['light-value']

                try:
                    actualValue = int(actual_value)
                except(ValueError):
                    actualValue = 0

                newValue = actualValue + stepValue
                if newValue < POTMETER_MIN:
                    newValue = POTMETER_MIN

                elif newValue > POTMETER_MAX:
                    newValue = POTMETER_MAX

                config_ini["light-value"] = newValue
                setConfigExchange(config_ini)

                Board.getInstance().setPwmByValue(id, newValue)

                print("                                      POST /actuator", "id=", id, "startValue=", actualValue, "stepValue=", stepValue, "newValue=", newValue)

            else:

                raise InvalidAPIUsage("No such actuator: {0} or step value: {1}".format(id, step_value), status_code=404)

            return {'status': 'OK'}














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
#
                config_ini = getConfigExchange()
                actual_value = config_ini['light-value']

                try:
                    actualValue = int(actual_value)
                except(ValueError):
                    actualValue = 0

                newValue = actualValue + stepValue
                if newValue < POTMETER_MIN:
                    newValue = POTMETER_MIN

                elif newValue > POTMETER_MAX:
                    newValue = POTMETER_MAX

                config_ini["light-value"] = newValue
                setConfigExchange(config_ini)

                thread = Thread(target = Board.getInstance().setPwmByStepValueGradually, args = (id, actualValue, newValue, inSeconds)) 
                thread.daemon = True
                thread.start()

                #Board.getInstance().setPwmByValue(id, newValue)

                print("                                      POST /actuator", "id=", id, "startValue=", actualValue, "stepValue=", stepValue, "newValue=", newValue)

            else:

                raise InvalidAPIUsage("No such actuator: {0} or step value: {1} or seconds {2}".format(id, step_value, in_seconds), status_code=404)

            return {'status': 'OK'}




#    ----------------

    # #################################################
    #
    # Shows any other Errors in application/json format
    #
    # #################################################
#    @app.errorhandler(Exception)
#    def handle_error(e):
#        if hasattr(e, 'code'):
#            code = e.code
#        else:
#            code = ""
#
#        return jsonify({"error": str(e)}), code, {'Content-Type': 'application/json'}


    def startService(self):

        # register the end-points
        self.ConfigView.register(app, None, None, None, None, None, "hello")
        self.ActuatorView.register(app)
        self.TemplateView.register(app)
        #self.TemplateView.register(app, route_base="/template")

serviceContrl = ServiceControl()
serviceContrl.startService()

if __name__ == '__main__':
    app.run(host= '0.0.0.0')

