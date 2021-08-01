import logging

class GradualThreadController(object):
    __instance = None

    def __new__(cls):
        if GradualThreadController.__instance is None:
            GradualThreadController.__instance = object.__new__(cls)
            #GradualThreadController.__instance.__init__() 
        return GradualThreadController.__instance

    @classmethod
    def getInstance(cls):
        inst = cls.__new__(cls)
        cls.__init__(cls.__instance) 
        return inst

    def __init__(self):
        self.shouldStop = False
        self.running = False

    def run(self, threadId):
        logging.debug( "Set Thread Started >")

        self.shouldStop = False
        self.running = True

    def isRunning(self):
        return self.running

    def stopRunning(self):
        self.running = False
        self.shouldStop = False

        logging.debug( "Set Thread Stopped <")

    def shouldItStop(self):
        return self.shouldStop
 
    def indicateToStop(self):
        self.shouldStop = True

