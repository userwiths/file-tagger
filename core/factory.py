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