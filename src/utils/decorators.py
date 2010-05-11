# -*- coding: utf-8 -*-

from utils.BridgeClass import BridgeClass

class debugPrint(BridgeClass):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        self.logprint("Running function:", self.func.__name__)
        ret = self.func(*args, **kwargs)
        self.logprint("Leaving function:", self.func.__name__)
        return ret

