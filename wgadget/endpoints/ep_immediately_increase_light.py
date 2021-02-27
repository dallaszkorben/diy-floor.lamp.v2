from exceptions.invalid_api_usage import InvalidAPIUsage
import logging

class EPImmediatelyIncreaseLight(object):

    NAME = 'increase_light_immediately'
    URL = '/immediately/increase'

    URL_ROUTE_PAR_PAYLOAD = '/increase'
    URL_ROUTE_PAR_URL = '/increase/actuatorId/<actuatorId>/stepValue/<stepValue>'

    METHOD = 'POST'

    ATTR_ACTUATOR_ID = 'actuatorId'
    ATTR_STEP_VALUE = 'stepValue'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    def getRequestDescriptionWithPayloadParameters(self):

        ret = {}
        ret['name'] = EPImmediatelyIncreaseLight.NAME
        ret['url'] = EPImmediatelyIncreaseLight.URL_ROUTE_PAR_PAYLOAD
        ret['method'] = EPImmediatelyIncreaseLight.METHOD

        ret['payload-desc'] = [{},{}]

        ret['payload-desc'][0]['attribute'] = EPImmediatelyIncreaseLight.ATTR_ACTUATOR_ID
        ret['payload-desc'][0]['type'] = 'integer'
        ret['payload-desc'][0]['value'] = 1


        ret['payload-desc'][1]['attribute'] = EPImmediatelyIncreaseLight.ATTR_STEP_VALUE
        ret['payload-desc'][1]['type'] = 'integer'
        ret['payload-desc'][1]['min'] = -100
        ret['payload-desc'][1]['max'] = 100

        return ret

    def executeByParameters(self, actuatorId, stepValue):
        payload = {}
        payload[EPImmediatelyIncreaseLight.ATTR_ACTUATOR_ID] = int(actuatorId)
        payload[EPImmediatelyIncreaseLight.ATTR_STEP_VALUE] = int(stepValue)
        self.executeByPayload(payload)


    def executeByPayload(self, payload):

        actuatorId = payload[EPImmediatelyIncreaseLight.ATTR_ACTUATOR_ID]
        stepValue = payload[EPImmediatelyIncreaseLight.ATTR_STEP_VALUE]

        actualValue = self.web_gadget.fetchLightValue()
        newValue = actualValue['current'] + stepValue
        newValue = min(100, newValue) if stepValue > 0 else max(0, newValue)

        if actuatorId == self.web_gadget.getLightId():

            logging.info( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5})".format(
                EPImmediatelyIncreaseLight.METHOD, EPImmediatelyIncreaseLight.URL,
                EPImmediatelyIncreaseLight.ATTR_ACTUATOR_ID, actuatorId,
                EPImmediatelyIncreaseLight.ATTR_STEP_VALUE, stepValue)
            )

            # Save the light value and set the Light
            self.web_gadget.setLight(newValue)

        else:
            raise InvalidAPIUsage("No such actuator: {0} or value: {1}".format(actuatorId, newValue), status_code=404)

        return {'status': 'OK'}

