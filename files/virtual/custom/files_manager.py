import re
from core import VirtualManager
from declaration import config,factory,VNode

class VirtualManager(VirtualManager):
    def __init__(self):
        self.index_manager = factory.getInstanceByName(config.indexManager)
        self.tag_manager = factory.getInstanceByName(config.tagsManager)

    def get_root_items(self):
        result = []
        for i in self.index_manager.get_indexed_files():
            vnode = i
            root = re.split(r' |/|\\',vnode.path)[0]
            
            if root not in result:
                result.append(root)

            if vnode.path.startswith(vnode.name):
                result.append(vnode)

        return result

    def get_all_items(self):
        return self.index_manager.get_indexed_files()

    def get_item(self, path:str):
        return [i for i in self.index_manager.get_indexed_files() if i.path==path]

    def get_children(self, path:str):
        return [r for r in self.index_manager.get_indexed_files() if r.path!=path and r.path.startswith(path)]

    def get_parent(self, path:str):
        files = self.index_manager.get_indexed_files()
        files = [i for i in files if path.startswith(i.path)]
        return files
        
    def is_traversable(self, path:str):
        return len([i for i in self.index_manager.get_indexed_files() if i.path.startswith(path) and i.path!=path])>0