from exceptions.invalid_api_usage import InvalidAPIUsage

class EPImmediatelyReverseLight(object):

    NAME = 'reverse_light_immediately'
    URL = '/immediately/reverse'

    URL_ROUTE_PAR_PAYLOAD = '/reverse'
    URL_ROUTE_PAR_URL = '/reverse/actuatorId/<actuatorId>'

    METHOD = 'POST'

    ATTR_ACTUATOR_ID = 'actuatorId'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    def getRequestDescriptionWithPayloadParameters(self):

        ret = {}
        ret['name'] = EPImmediatelyReverseLight.NAME
        ret['url'] = EPImmediatelyReverseLight.URL_ROUTE_PAR_PAYLOAD
        ret['method'] = EPImmediatelyReverseLight.METHOD

        ret['payload-desc'] = [{}]

        ret['payload-desc'][0]['attribute'] = EPImmediatelyReverseLight.ATTR_ACTUATOR_ID
        ret['payload-desc'][0]['type'] = 'integer'
        ret['payload-desc'][0]['value'] = 1

        return ret

    def executeByParameters(self, actuatorId):

        payload = {}
        payload[EPImmediatelyReverseLight.ATTR_ACTUATOR_ID] = int(actuatorId)
        self.executeByPayload(payload)


    def executeByPayload(self, payload):

        actuatorId = payload[EPImmediatelyReverseLight.ATTR_ACTUATOR_ID]

        if actuatorId == self.web_gadget.getLightId():

            # Save the light value and set the Light
            self.web_gadget.reverseLight()

        else:
            raise InvalidAPIUsage("No such actuator: {0}".format(actuatorId), status_code=404)
