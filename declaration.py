import re
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
        
factory=Factory()
config=ConfigAdvanced()