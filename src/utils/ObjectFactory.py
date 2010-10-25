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

class ObjectFactoryError(Exception):
    """
    Default Object Factory Exception.
    """

class OFModuleNotLoadedError(ObjectFactoryError):
    """
    Couldn't load module.
    """

class OFClassNotInModuleError(ObjectFactoryError):
    """
    Class not found in module.
    """

class OFClassNotFoundError(ObjectFactoryError):
    """
    Class with given name wasn't found.
    """

class OFWrongBaseClassError(ObjectFactoryError):
    """
    Class found, but doesn't have the correct base class.
    """

class ObjectFactory(object):
    def create(self, classname, mod=None, inst=None, args=None):
        # Dynamically load module.
        if mod:
            modulename = mod + '.' + classname
            module = __import__(modulename, globals(), locals(), [classname], -1)
        else:
            modulename = classname
            module = __import__(modulename)
        if not module:
            print "Couldn't load module:", modulename
            raise OFModuleNotLoadedError

        # Check that module has classname defined.
        moddir = dir(module)
        #print "moddir:", moddir
        if classname not in moddir:
            raise OFClassNotInModuleError

        # Dynamically create a class reference.
        cls = getattr(module, classname)
        #print "dircls:", dir(cls)
        if not cls:
            raise OFClassNotFoundError

        # Cover our bases, make sure class is of correct instance.
        if inst:
            found = None
            for b in cls.__bases__:
                if inst == b.__name__:
                    found = True
                    continue
            if not found:
                raise OFWrongBaseClassError

        # Return an instance object of the class.
        return cls(args)

if __name__ == '__main__':
    xml = loadUrl('http://www.rollspel.nu/forum/ubbthreads.php?ubb=listshouts')
    parser = ElementParser()
    dom = parser(xml)

