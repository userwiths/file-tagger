import re
from functools import wraps
from core import Factory,ConfigAdvanced

class VNode:
    def __init__(self):
        self.path=''
        self.name=''
        self.value=0
        self.other={}

    def build(self,data):
        self.value=data.split(';')[1]
        self.path=data.split(';')[0]
        self.name=re.split(r' |/|\\',self.path)[-1:]
        self.name=self.name[0]

        return self
        
cache=[
    {'name':'TagManager','method':'load_tags','store':None},
    {'name':'IndexManager','method':'load_files','store':None},
    {'name':'TagManager','method':'load_tags','store':None}
]

def invalidate(func):
    @wraps(func)    
    def execute_and_invalidate(*args, **kwargs):
        func(*args, **kwargs)
        print(factory.getInstanceByName('TagManager').load_tags())
        print('\n')
    return execute_and_invalidate

factory=Factory()
config=ConfigAdvanced()