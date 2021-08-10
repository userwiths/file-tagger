import re

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

class Config:
    def __init__(self):
        self.name=''
        self.description=''
        self.options=[]

        self.persistent=False
        self.config_file=''
        self.config_directory=''

class Option:
    def __init__(self):
        self.name=''
        self.description=''
        self.default_value=''

class ConfigAdvanced:
    def __init__(self):
        self.indexModule='index'
        self.tagModule='tags'

        self.indexManager='IndexManager'
        self.tagsManager='TagManager'

        self.index=('index',self.indexManager)
        self.tags=('tags',self.tagsManager)
        self.realFiles=('files','FileManager')
        self.virtualFiles=('files','VirtualManager')

        self.tagsFile='tags.txt'
        self.indexFile='index.txt'

        self.commentSymbol="#"

class Factory:
    def __init__(self):
        # {NAME:INSTANCE}
        self.register=[]

    def setInstance(self,obj):
        self.register.append({
            'name':obj.__class__.__name__,
            'instance':obj
        })

    def getInstanceByName(self,className):
        for i in self.register:
            if i['name']==className:
                return i['instance']

    def create(self,module_name,class_name):
        module = __import__(module_name)
        class_ = getattr(module, class_name)
        instance = class_()

        self.register.append({'name':class_name,'instance':instance})
        return instance

    def createWith(self,module_name,class_name,dependancy_list):
        module = __import__(module_name)
        class_ = getattr(module, class_name)

        dependencies=[]
        
        instance = class_(self.getInstanceByName(dependancy_list))

        self.register.append({'name':class_name,'instance':instance})
        return instance
        
factory=Factory()
config=ConfigAdvanced()