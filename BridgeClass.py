# -*- coding: utf-8 -*-

from datetime import datetime

class BridgeClass:
    def mixinMethod(self, method, name=None):
        """
        Mixin method into this class, under name.
        ** BROKEN **
        """
        if name is None:
            name = method.__name__
        print "Mixin method:", name, method
        self.__setitem__(name, method)
        return
        class new(self.__class__):
            pass
        setattr(new, name, method)
        self.__class__ = new

    def mixinClass(self, cls):
        """
        Mixin methods from cls into this class.
        Don't use, use MixIn class from Linux Journal instead.
        """
        #class new(self, cls):
        #    pass
        #self.__class__ = new
        #return
        attrs = vars(cls)
        for k, v in attrs.items():
            #if k not in self.__dict__ and callable(v):
            print "attr:", k, v
            if not k.startswith('__'):
                m = getattr(cls, k)
                if type(m) is types.MethodType:
                    print "Mixing in:", v
                    setattr(self, k, m)

    def logprint(self, *message):
        #print "--------------------------------------------------------------"
        print datetime.now().strftime(self.cfg.log_date_format), '-',
        for m in message:
            print m,
        print "\n--------------------------------------------------------------"

    def print_items(self, items):
        """
        Returns all items as a string in a neat table.
        """
        str = ''
        for k, v in items:
            str += string.ljust(k, 15) + '\t' + unicode(v) + '\n'
        return str

    def dumpall(self):
        """
        Return all instance attributes and methods in readable format.
        """
        return self.print_items(self.__dict__.items() + self.__class__.__dict__.items())

    def __str__(self):
        """
        Return all instance attributes in readable format.
        """
        return self.print_items(self.__dict__.items())

def main():
    import sys
    import string

# Call the main function.
if __name__ == '__main__':
    main()
