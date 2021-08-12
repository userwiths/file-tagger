from functools import wraps

cache=[
    {'name':'TagManager','method':'load_tags','store':None},
    {'name':'IndexManager','method':'load_files','store':None},
    {'name':'TagManager','method':'load_tags','store':None}
]

def invalidate(func):
    @wraps(func)    
    def execute_and_invalidate(*args, **kwargs):
        func(*args, **kwargs)
        print(dir(func))
        print("Module: "+func.__module__)
        print("Class: "+func.__class__.__name__)
        print("Name: "+func.__name__)
    return execute_and_invalidate

class CacheRecord:
    def __init__(self,name,method):
        self.name=name
        self.reload=method
        self.store=None
        self.invalidator=[]

    def register(self,className,invalidator):
        if invalidator not in self.invalidator:
            self.invalidator.append({'method':invalidator,'class':className})

class CacheManager:
    def __init__(self):
        # name -> generic identifier used to reference the section, preferably name of class
        # reload -> operation to execute on invalidate
        # cache store -> place where the data returned from 'reload' is stored as cache
        self.sections=[]

    def register(self,name,className,method):
        record=CacheRecord(name,className,method)
        self.sections.append(record)

    def relay(self,originalMethod,relayMethod,args):
        originalMethod(*args)
        relayMethod()

    def invalidator(self,method,args):
        method(*args)

        class_name=method.__self__.__class__.__name__
        
        for section in self.sections:
            invalidators=[i for i in section.invalidator if i['class']==class_name and i['method']==method.__name__]
            if len(invalidators)>0:
                invalidate()

    def invalidate(self,section=None):
        pass