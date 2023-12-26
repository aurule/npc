class Singleton(type):
    """
    Metaclass for creating singleton classes.

    Usage:
        def ClassName(metaclass=Singleton):
            ...

        obj = ClassName()   # creates the object
        obj2 = ClassName()  # returns the same object
        obj is obj2         # True

    For testing, the clearSingleton argument can be set to True to force the constructor to create a new object
    """
    _instances = {}
    def __call__(cls, *args, clearSingleton: bool = False, **kwargs):
        if cls not in cls._instances or clearSingleton:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
