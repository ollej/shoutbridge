# -*- coding: utf-8 -*-

from datetime import datetime
import string

class BridgeClass(object):
    def logprint(self, *message):
        if self.cfg and not self.cfg.get_bool('verbose'):
            return
        #print "--------------------------------------------------------------"
        try:
            date_format = self.cfg.log_date_format
        except AttributeError:
            date_format = "%Y-%m-%d %H:%M:%S"
        print datetime.now().strftime(date_format), '-',
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
