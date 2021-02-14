import json
from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from wgadget.representations import output_json

from threading import Thread

from egadget.eg_light import EGLight

from config.config_exchange import getConfigExchange
from config.config_exchange import setConfigExchange
from config.config_egadget import getConfigEGadget

# -----------------------------------
#
# POST Contorl the level of the light
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/immediately/set/actuator/1/value/10
# curl  --header "Content-Type: application/json" --request POST --data '{"actuator":"1","value":"10"}' http://localhost:5000/immediately/set
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/immediately/increase/actuator/1/stepvalue/-10
# curl  --header "Content-Type: application/json" --request POST --data '{"actuator":"1","stepValue":"-10"}' http://localhost:5000/immediately/increase
#
# -----------------------------------
#
# GET http://localhost:5000/immediately
class ImmediatelyView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, parent):
        self.parent = parent

    #
    # GET http://localhost:5000/set/
    #
    def index(self):
        return {}

    #
    # Set the light value immediately
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/immediately/set/actuator/1/value/10
    #
    # POST http://localhost:5000/immediately/set/actuator/1/value/10
    #
    @route('/set/actuator/<actuator>/value/<value>', methods=['POST'])
    def set(self, actuator, value):

        try:
            actuatorId = int(actuator)
            value = int(value)
        except(ValueError):
            actuatorId = -1

        # actuator #1 => Light
        if actuatorId == 1:

            if value >= 0 and value <= 100:

                actualValue = self.parent.fetchLightValue()

                if value == 0 and actualValue['current']:

                    # Save the light value and set the Light
                    self.parent.setLight(value, actualValue['current'])

                else:
                    # Save the light value and set the Light
                    self.parent.setLight(value)

                print("                                      POST /actuator", "id=", id, "value=", value)

            else:
                raise InvalidAPIUsage("The value is not valid: {0}".format(value), status_code=404)

        else:
            raise InvalidAPIUsage("No such actuator: {0} or value: {1}".format(id, value), status_code=404)

        return {'status': 'OK'}

    #
    # Set the light value immediately with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"actuator":"1","value":"10"}' http://localhost:5000/imediately/set
    #
    # POST http://localhost:5000/imediately/set
    #      body: {
    #                'actuator': "1',
    #                'value: '13'
    #           }
    #
    @route("/set",  methods=['POST'] )
    def setWithPayload(self):

        # WEB
        if request.form:

            if 'actuator' in request.form:
                print('actuator', request.form['actuator'])
            if 'value' in request.form:
                print('value', request.form['value'])

            actuator = request.form['actuator']
            value = request.form['value']

        # CURL
        elif request.json:

            json_data = request.json
            actuator = json_data["actuator"]
            value = json_data["value"]

        else:
            return {}

        print(actuator, value)
        return self.set(actuator, value)

# ---

    #
    # Increase the light value immediately
    #
    # POST http://localhost:5000/imediately/increase/actuator/1/stepvalue/-10
    #
    #
    @route('/increase/actuator/<actuator>/stepvalue/<step_value>', methods=['POST'])
    def increase(self, actuator, step_value):

        try:
            actuatorId = int(actuator)
            stepValue = int(step_value)
        except(ValueError):
            actuatorId = -1

        # actuator #1 => Light
        if actuatorId == 1:

            actualValue = self.parent.fetchLightValue()

#            try:
#                actualValue = int(actual_value)
#            except(ValueError):
#                actualValue = 0

            newValue = actualValue['current'] + stepValue
            newValue = min(100, newValue) if stepValue > 0 else max(0, newValue)

            # Save the light value and set the Light
            self.parent.setLight(newValue)

            print("                                      POST /actuator", "actuatorId=", actuatorId, "value=", newValue)

        else:
            raise InvalidAPIUsage("No such actuator: {0} or value: {1}".format(id, newValue), status_code=404)

        return {'status': 'OK'}

    #
    # Increase the light value immediately with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"actuator":"1","stepValue":"-10"}' http://localhost:5000/imediately/increase
    #
    # POST http://localhost:5000/imediately/increase
    #      body: {
    #                'actuator': "1',
    #                'stepValue: '-10'
    #           }
    #
    @route("/increase",  methods=['POST'] )
    def increaseWithPayload(self):

        # WEB
        if request.form:

            if 'actuator' in request.form:
                print('actuator', request.form['actuator'])
            if 'stepValue' in request.form:
                print('stepValue', request.form['stepValue'])

            actuatorId = request.form['actuator']
            stepValue = request.form['stepValue']

        # CURL
        elif request.json:

            json_data = request.json
            actuatorId = json_data["actuator"]
            stepValue = json_data["stepValue"]

        else:
            return {}

        print(actuatorId, stepValue)
        return self.increase(actuatorId, stepValue)
