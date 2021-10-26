
import logging
from threading import Thread
from threading import get_ident
from exceptions.invalid_api_usage import InvalidAPIUsage
from wgadget.endpoints.ep import EP
from time import sleep

class EPSignalSend(EP):

    NAME = 'signal_send'
    URL = '/signal/send'

    URL_ROUTE_PAR_PAYLOAD = '/send'
    URL_ROUTE_PAR_URL = '/send/actuatorId/<actuatorId>/signalId/<signalId>'

    METHOD = 'POST'

    ATTR_ACTUATOR_ID = 'actuatorId'
    ATTR_SIGNAL_ID = 'signalId'

    TIME_WAIT_FOR_THREAD = 0.5

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    def getRequestDescriptionWithPayloadParameters(self):

        ret = {}
        ret['name'] = EPSignalSend.NAME
        ret['url'] = EPSignalSend.URL_ROUTE_PAR_PAYLOAD
        ret['method'] = EPSignalSend.METHOD

        ret['payload-desc'] = [{},{},{}]

        ret['payload-desc'][0]['attribute'] = EPSignalSend.ATTR_ACTUATOR_ID
        ret['payload-desc'][0]['type'] = 'integer'
        ret['payload-desc'][0]['value'] = 1

        ret['payload-desc'][1]['attribute'] = EPSignalSend.ATTR_SIGNAL_ID
        ret['payload-desc'][1]['type'] = 'integer'
        ret['payload-desc'][1]['min'] = 0
        ret['payload-desc'][1]['max'] = 100

        return ret

    def executeByParameters(self, actuatorId, signalId):
        payload = {}
        payload[EPSignalSend.ATTR_ACTUATOR_ID] = int(actuatorId)
        payload[EPSignalSend.ATTR_SIGNAL_ID] = int(signalId)
        self.executeByPayload(payload)


    def executeByPayload(self, payload):

        actuatorId = int(payload[EPSignalSend.ATTR_ACTUATOR_ID])
        signalId = int(payload[EPSignalSend.ATTR_SIGNAL_ID])

        if actuatorId == self.web_gadget.getLightId():

            # Stop the running Thread
            self.web_gadget.gradualThreadController.indicateToStop()
            while self.web_gadget.gradualThreadController.isRunning():
                logging.debug( "  Waitiong for thread stops in {0} in executedByPayload() method".format(__file__))
                sleep(self.__class__.TIME_WAIT_FOR_THREAD)

            actualValue = self.web_gadget.fetchSavedLightValue()

            logging.debug( "{0} {1} ('{2}': {3}, '{4}': {5})".format(
                        EPSignalSend.METHOD, EPSignalSend.URL,
                        EPSignalSend.ATTR_ACTUATOR_ID, actuatorId,
                        EPSignalSend.ATTR_SIGNAL_ID, signalId)
            )

            thread = Thread(target = self.runThread, args = (signalId, actualValue['current']))


            thread.daemon = True
            thread.start()

        else:
            raise InvalidAPIUsage("No such actuator: {0} or signal type: {1}}".format(actuatorId, signalId), error_code=404)

        return {'status': 'OK'}

    # THREAD
    def runThread(self, signalId, currentId):

        self.web_gadget.gradualThreadController.run(get_ident())

        self.web_gadget.sendSignal(signalId);

        self.web_gadget.gradualThreadController.stopRunning()
