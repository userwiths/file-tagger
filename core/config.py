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
        self.fileHandler=('files','FileHandler')

        self.tagsFile='tags.txt'
        self.indexFile='index.txt'

        self.commentSymbol="#"
