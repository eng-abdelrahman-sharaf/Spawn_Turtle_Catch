class SingletonClass:
    _instance = None
    def __new__(cls , *args, **kwargs):
        if cls._instance is None:
            instance = object.__new__(cls)
            instance._singleton_init(*args, **kwargs)
            cls._instance = instance
        else: 
            if len(args):
                raise Exception("Can't create another instance Use ClassName([no args]) to get the singleton instance")
        return cls._instance

    def __init__(self , *args , **kwargs):
        if(self._instance != None): return
    def _singleton_init(self , *args , **kwargs):
        pass
