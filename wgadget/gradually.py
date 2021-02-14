from datetime import datetime
#import tzlocal
#import time

import json
from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from wgadget.exceptions import InvalidAPIUsage

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
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/gradually/set/actuator/1/value/10/inseconds/3
# curl  --header "Content-Type: application/json" --request POST --data '{"actuator":"1","value":"10","inSeconds":"3"}' http://localhost:5000/gradually/set
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/gradually/increase/actuator/1/stepvalue/-10/inseconds/3
# curl  --header "Content-Type: application/json" --request POST --data '{"actuator":"1","stepValue":"-10","inSeconds":"3"}' http://localhost:5000/gradually/increase
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/gradually/schedule/set/actuator/1/value/100/inseconds/3/fromdatetime/2021-02-14T21:15:00
# curl  --header "Content-Type: application/json" --request POST --data '{"actuator":"1","value":"10","inSeconds":"3","fromDateTime":"2021-02-14T21:15:00"}' http://localhost:5000/gradually/schedule/set
#
# -----------------------------------
#
# GET http://localhost:5000/gradually
class GraduallyView(FlaskView):
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
    # Set the light value gradually
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/gradually/set/actuator/1/value/10/inseconds/3
    #
    # POST http://localhost:5000/gradually/set/actuator/1/value/10/inseconds/3
    #
    @route('/set/actuator/<actuator>/value/<value>/inseconds/<in_seconds>', methods=['POST'])
    def set(self, actuator, value, in_seconds):

        try:
            actuatorId = int(actuator)
            value = int(value)
            inSeconds = int(in_seconds)
        except(ValueError):
            actuatorId = -1

        # actuator #1 => Light
        if actuatorId == 1:

            if value >= 0 and value <= 100:

                actualValue = self.parent.fetchLightValue()
                newValue = value

                # Save the light value and set the Light
                thread = Thread(target = self.parent.setLightGradually, args = (actuatorId, actualValue['current'], newValue, inSeconds)) 
                thread.daemon = True
                thread.start()

                print("                                      POST /actuator", "actuatorId=", actuatorId, "startValue=", actualValue['current'], "newValue=", newValue, "inSeconds=", inSeconds)

            else:
                raise InvalidAPIUsage("The value is not valid: {0}".format(value), status_code=404)

        else:
            raise InvalidAPIUsage("No such actuator: {0} or value: {1}".format(actuatorId, value), status_code=404)

        return {'status': 'OK'}

    #
    # Set the light value gradually with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"actuator":"1","value":"10","inSeconds":"3"}' http://localhost:5000/gradually/set
    #
    # POST http://localhost:5000/gradually/set
    #      body: {
    #                'actuator': "1',
    #                'value: '13'
    #                'inSeconds: '-3'
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
            if 'inSeconds' in request.form:
                print('inSeconds', request.form['inSeconds'])

            actuatorId = request.form['actuator']
            value = request.form['value']
            inSeconds = request.form['inSeconds']

            print("web")

        # CURL
        elif request.json:

            json_data = request.json
            actuatorId = json_data["actuator"]
            value = json_data["value"]
            inSeconds = json_data["inSeconds"]

        else:
            return {}

        print(actuatorId, value, inSeconds)
        return self.set(actuatorId, value, inSeconds)

# ---

    #
    # Increase the light value gradually
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"actuator":"1","value":"10"}' http://localhost:5000/gradually/increase/actuator/1/stepvalue/-10/inseconds/3
    #
    #
    @route('/increase/actuator/<actuator>/stepvalue/<step_value>/inseconds/<in_seconds>', methods=['POST'])
    def increase(self, actuator, step_value, in_seconds):

        try:
            actuatorId = int(actuator)
            stepValue = int(step_value)
            inSeconds = int(in_seconds)
        except(ValueError):
            actuatorId = -1

        # actuator #1 => Light
        if actuatorId == 1:

            actualValue = self.parent.fetchLightValue()

            newValue = actualValue['current'] + stepValue
            newValue = min(100, newValue) if stepValue > 0 else max(0, newValue)

            thread = Thread(target = self.parent.setLightGradually, args = (id, actualValue['current'], newValue, inSeconds)) 
            thread.daemon = True
            thread.start()

            print("                                      POST /actuator", "id=", id, "startValue=", actualValue, "stepValue=", stepValue, "newValue=", newValue)

        else:
            raise InvalidAPIUsage("No such actuator: {0} or step value: {1} or seconds {2}".format(id, step_value, in_seconds), status_code=404)

        return {'status': 'OK'}

    #
    # Increase the light value gradually with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"actuator":"1","stepValue":"-10","inSeconds":"3"}' http://localhost:5000/gradually/increase
    #
    #      body: {
    #                'actuator': "1',
    #                'stepValue: '-10'
    #                'inSeconds: '3'
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
            if 'inSeconds' in request.form:
                print('inSeconds', request.form['inSeconds'])

            actuatorId = request.form['actuator']
            stepValue = request.form['stepValue']
            inSeconds = request.form['inSeconds']

        # CURL
        elif request.json:

            json_data = request.json
            actuatorId = json_data["actuator"]
            stepValue = json_data["stepValue"]
            inSeconds = json_data["inSeconds"]

        else:
            return {}

        print(actuatorId, stepValue, inSeconds)
        return self.increase(actuatorId, stepValue, inSeconds)


# ---


    #
    # Set the light value gradually in a scheduled time
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/gradually/schedule/set/actuator/1/value/100/inseconds/3/at/2021-02-14T21:15:00
    #
    # POST http://localhost:5000/gradually/schedule/set/actuator/1/value/100/inseconds/3/at/2021-02-14T21:15:00+01:00
    #
    @route('schedule/set/actuator/<actuator>/value/<value>/inseconds/<in_seconds>/at/<isoformat_at_date_time>', methods=['POST'])
    def scheduleSet(self, actuator, value, in_seconds, isoformat_at_date_time):

        try:
            actuatorId = int(actuator)
            value = int(value)
            inSeconds = int(in_seconds)
            atDateTime = datetime.fromisoformat(isoformat_at_date_time)
        except(ValueError):
            actuatorId = -1

        # actuator #1 => Light
        if actuatorId == 1:

            if value >= 0 and value <= 100:

#                timeZone = tzlocal.get_localzone()
#                zoneName = timeZone.zone

#                atDateTime=atDateTime.astimezone(timeZone).replace(microsecond=0)
#
#                while True:
#                    time.sleep(1)
#                    nowDateTime=datetime.now().astimezone(timeZone).replace(microsecond=0)
#                    if nowDateTime >= fromDateTime:
#                        break

#                actualValue = self.parent.fetchLightValue()
#                newValue = value

                # Save the light value and set the Light
                thread = Thread(target = self.parent.setLightScheduledGradually, args = (actuatorId, value, inSeconds, atDateTime)) 
                thread.daemon = True
                thread.start()

                print("                                      POST /actuator", "actuatorId=", actuatorId, "startValue=", "value=", value, "inSeconds=", inSeconds, "at=", atDateTime)

            else:
                raise InvalidAPIUsage("The value is not valid: {0}".format(value), status_code=404)

        else:
            raise InvalidAPIUsage("No such actuator: {0} or value: {1} or in_seconds: {2} or at: {3}".format(actuator, value, in_seconds, isoformat_at_date_time), status_code=404)

        return {'status': 'OK'}

    #
    # Set the light value gradually in a scheduled time
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"actuator":"1","value":"10","inSeconds":"3","at":"2021-02-14T21:15:00"}' http://localhost:5000/gradually/schedule/set
    #
    # POST http://localhost:5000/gradually/schedule/set
    #      body: {
    #                'actuator': "1',
    #                'value: '13'
    #                'inSeconds: '-3',
    #                "at":"2021-02-14T21:15:00"
    #           }
    #
    @route("/schedule/set",  methods=['POST'] )
    def scheduleSetWithPayload(self):

#        print("request.form", request.form)
#        print("request.json", request.json)
        print("!!!!!!!!!!!!!!! HAHO !!!!!!!!!!!!!!1")
        # WEB
        if request.form:

            if 'actuator' in request.form:
                print('actuator', request.form['actuator'])
            if 'value' in request.form:
                print('value', request.form['value'])
            if 'inSeconds' in request.form:
                print('inSeconds', request.form['inSeconds'])
            if 'at' in request.form:
                print('at', request.form['at'])

            actuatorId = request.form['actuator']
            value = request.form['value']
            inSeconds = request.form['inSeconds']
            at = request.form['at']

        # CURL
        elif request.json:

            json_data = request.json
            actuatorId = json_data["actuator"]
            value = json_data["value"]
            inSeconds = json_data["inSeconds"]
            at = json_data["at"]

        else:
            return {}

        print(actuatorId, value, inSeconds, at)
        return self.scheduleSet(actuatorId, value, inSeconds, at)





