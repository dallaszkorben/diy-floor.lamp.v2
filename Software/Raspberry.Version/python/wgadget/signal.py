import json
from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

#from wgadget.exceptions import InvalidAPIUsage
from exceptions.invalid_api_usage import InvalidAPIUsage

from wgadget.representations import output_json

from threading import Thread

from egadget.eg_light import EGLight

from config.config_exchange import getConfigExchange
from config.config_exchange import setConfigExchange
from config.config_egadget import getConfigEGadget

from wgadget.endpoints.ep_signal_light import EPSignalSend


# -----------------------------------
#
# POST Send Signal
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/signal/send/actuatorId/1/signalId/10
# curl  --header "Content-Type: application/json" --request POST --data '{"actuatorId":1,"value":10,"signalId":3}' http://localhost:5000/signal/send
#
# -----------------------------------
#
# GET http://localhost:5000/signal
class SignalView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

        self.epSignalSend = EPSignalSend(web_gadget)

    #
    # GET http://localhost:5000/signal/
    #
    def index(self):
        return {}

# ===

    #
    # Send Signal
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"actuatorId":1, "signalId":3}' http://localhost:5000/signal/send
    #
    # POST http://localhost:5000/signal/send
    #      body: {
    #                'actuatorId': "1',
    #                'signalId: '3'
    #           }
    #
    @route("/send",  methods=['POST'] )
    def sendWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return {}

        self.epSignalSend.executeByPayload(json_data)

        return {'status': 'OK'}

    #
    # Send signal
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/signal/send/actuatorId/1/signalId/10
    #
    # POST http://localhost:5000/signal/send/actuatorId/1/signalId/3
    #
    #@route('/send/actuatorId/<actuatorId>/signalId/<signalId>', methods=['POST'])
    @route(EPSignalSend.URL_ROUTE_PAR_URL, methods=[EPSignalSend.METHOD])
    def send(self, actuatorId, signalId):

        self.epSignalSend.executeByParameters(actuatorId=actuatorId, signalId=signalId)

        return {'status': 'OK'}

