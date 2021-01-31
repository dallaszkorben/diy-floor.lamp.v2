#! /usr/bin/python3

import json
from flask import Flask
from flask import jsonify
from flask_classful import FlaskView, route, request
from representations import output_json


from config_exchange import getConfig
from config_exchange import setConfig

app = Flask(__name__)

class InvalidAPIUsage(Exception):
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        if status_code is not None:
            self.code = status_code
        else:
            self.code = 400
        self.payload = payload

class ServiceControl:

    # ---------------------------------
    #
    # GET Configuration Information
    #
    # ---------------------------------
    # GET http://localhost:5000/config
    class ConfigView(FlaskView):
        representations = {'application/json': output_json}

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
            config_ini = getConfig()
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
            config_ini = getConfig()
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

                config_ini = getConfig()
                config_ini["light-value"] = value
                setConfig(config_ini)

                print("POST /actuator", "id=", id, "value=",value)

            else:

                raise InvalidAPIUsage("No such actuator: {0}".format(id), status_code=404)

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
            json_data = request.json
            id = json_data.get("id")
            value = json_data.get("value")

            return self.post(id, value)

#    ----------------

    # #################################################
    #
    # Shows any other Errors in application/json format
    #
    # #################################################
    @app.errorhandler(Exception)
    def handle_error(e):
        if hasattr(e, 'code'):
            code = e.code
        else:
            code = ""

        return jsonify({"error": str(e)}), code, {'Content-Type': 'application/json'}


    def startService(self):

        # register the end-points
        self.ConfigView.register(app)
        self.ActuatorView.register(app)
        self.TemplateView.register(app)
        #self.TemplateView.register(app, route_base="/template")

serviceContrl = ServiceControl()
serviceContrl.startService()

if __name__ == '__main__':
    app.run()

