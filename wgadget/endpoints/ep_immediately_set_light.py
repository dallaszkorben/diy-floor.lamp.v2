
import logging
from exceptions.invalid_api_usage import InvalidAPIUsage

class EPImmediatelySetLight(object):

    NAME = 'set_light_immediately'
    URL = '/immediately/set'

    URL_ROUTE_PAR_PAYLOAD = '/set'
    URL_ROUTE_PAR_URL = '/set/actuatorId/<actuatorId>/value/<value>'

    METHOD = 'POST'

    ATTR_ACTUATOR_ID = 'actuatorId'
    ATTR_VALUE = 'value'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    def getRequestDescriptionWithPayloadParameters(self):

        ret = {}
        ret['name'] = EPImmediatelySetLight.NAME
        ret['url'] = EPImmediatelySetLight.URL_ROUTE_PAR_PAYLOAD
        ret['method'] = EPImmediatelySetLight.METHOD

        ret['payload-desc'] = [{},{}]

        ret['payload-desc'][0]['attribute'] = EPImmediatelySetLight.ATTR_ACTUATOR_ID
        ret['payload-desc'][0]['type'] = 'integer'
        ret['payload-desc'][0]['value'] = 1


        ret['payload-desc'][1]['attribute'] = EPImmediatelySetLight.ATTR_VALUE
        ret['payload-desc'][1]['type'] = 'integer'
        ret['payload-desc'][1]['min'] = 0
        ret['payload-desc'][1]['max'] = 100

        return ret

    def executeByParameters(self, actuatorId, value):
        payload = {}
        payload[EPImmediatelySetLight.ATTR_ACTUATOR_ID] = int(actuatorId)
        payload[EPImmediatelySetLight.ATTR_VALUE] = int(value)
        self.executeByPayload(payload)


    def executeByPayload(self, payload):

        actuatorId = payload[EPImmediatelySetLight.ATTR_ACTUATOR_ID]
        value = payload[EPImmediatelySetLight.ATTR_VALUE]

        if actuatorId == self.web_gadget.getLightId():

            if value >= 0 and value <= 100:

                actualValue = self.web_gadget.fetchLightValue()

                if value == 0 and actualValue['current']:

                    # Save the light value and set the Light
                    self.web_gadget.setLight(value, actualValue['current'])

                else:

                    # Save the light value and set the Light
                    self.web_gadget.setLight(value)

                    logging.info( "{0} {1} ('{2}': {3}, '{4}': {5})".format(
                        EPImmediatelySetLight.METHOD, EPImmediatelySetLight.URL,
                        EPImmediatelySetLight.ATTR_ACTUATOR_ID, actuatorId,
                        EPImmediatelySetLight.ATTR_VALUE, value)
                    )

            else:
                raise InvalidAPIUsage("The value is not valid: {0}".format(value), status_code=404)

        else:
            raise InvalidAPIUsage("No such actuator: {0} or value: {1}".format(actuatorId, value), status_code=404)
