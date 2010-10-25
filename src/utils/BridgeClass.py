# -*- coding: utf-8 -*-

"""
The MIT License

Copyright (c) 2010 Olle Johansson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from datetime import datetime
import string

class BridgeClass(object):
    def logprint(self, *message):
        try:
            if not self.cfg.get_bool('verbose'):
                return
        except AttributeError:
            pass
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

    def dumpattrs(self):
        """
        Return all instance attributes in readable format.
        """
        return self.print_items(self.__dict__.items())

    def __str__(self):
        """
        Return all instance attributes in readable format.
        """
        return self.dumpattrs()

def main():
    import sys
    import string

# Call the main function.
if __name__ == '__main__':
    main()
