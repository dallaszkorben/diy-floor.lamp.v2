from abc import abstractmethod

class SA:

    def configure(self):
        raise NotImplementedError

    def unconfigure(self):
        raise NotImplementedError
