import uuid,os, sys,subprocess
from core import FileManager

class FileManager(FileManager):
    """
    This class is an abstraction responsible for providing basic information about the REAL file system.
    """
    def __init__(self):
        pass

    def get_children(self, path:str):
        """ 
        In case the given 'path' is traversible
        Returns the 'children' of the given 'path'.
        """
        if self.is_traversable(path):
            return os.listdir(path)
        return []

    def get_parent(self, path:str):
        """ 
        Returns one level lower path.
        get_parent('/1/2/3/4/5') will return '\\1\\2\\3\\4'
        """
        pathArray=re.split(r' |/|\\', path)[:-1]
        return os.sep.join(pathArray)
        
    def is_traversable(self, path:str):
        """
        Returns if the path is traversible.
        """
        return os.path.isdir(path)