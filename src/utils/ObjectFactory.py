# -*- coding: utf-8 -*-

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

class ObjectFactory:
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
        print "moddir:", moddir
        if classname not in moddir:
            raise OFClassNotInModuleError

        # Dynamically create a class reference.
        cls = getattr(module, classname)
        print "dircls:", dir(cls)
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

