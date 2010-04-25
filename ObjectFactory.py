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
    def create(self, classname, inst=None):
        # Dynamically load module.
        module = __import__(classname)
        if not module:
            print "Couldn't load module:", classname
            raise OFModuleNotLoadedError

        # Check that module has classname defined.
        moddir = dir(module)
        if not classname in moddir:
            raise OFClassNotInModuleError

        # Dynamically create a class reference.
        #cls = globals()[classname]
        #cls = module[classname]
        cls = getattr(module, classname)
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
        return cls()

if __name__ == '__main__':
    xml = loadUrl('http://www.rollspel.nu/forum/ubbthreads.php?ubb=listshouts')
    parser = ElementParser()
    dom = parser(xml)

