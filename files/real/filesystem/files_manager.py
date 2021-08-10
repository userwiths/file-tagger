import uuid,os, sys,subprocess

class FileManager:
    def __init__(self):
        pass

    def get_children(self,path):
        if self.is_traversable(path):
            return os.listdir(path)
        return []

    def get_parent(self,path):
        pathArray=re.split(r' |/|\\',path)[:-1]
        return '\\'.join(pathArray)
        
    def is_traversable(self,path):
        return os.path.isdir(path)