import re
import os
from declaration import config,factory,VNode

class VirtualManager:
    def __init__(self):
        self.index_manager = factory.getInstanceByName(config.indexManager)
        self.tag_manager = factory.getInstanceByName(config.tagsManager)

    def get_root_items(self):
        result=  []
        for i in self.index_manager.get_indexed_files():
            vnode=VNode().build(i)
            root=re.split(r' |/|\\',vnode.path)[0]
            
            if root not in result:
                result.append(root)

            if vnode.path.startswith(vnode.name):
                result.append(vnode)

        return result

    def get_all_items(self):
        temp=self.index_manager.get_indexed_files()
        return [VNode().build(i) for i in temp]

    def get_item(self,path):
        return [VNode().build(i) for i in self.index_manager.get_indexed_files() if i.count(path)>0]

    def get_children(self,path):
        result = [VNode().build(i) for i in self.index_manager.get_indexed_files() if i.count(path)>0]
        return [r for r in result if result.path!=path and result.path.count(path)>0]

    def get_parent(self,path):
        i = -1
        parts = re.split(r' |/|\\',path)
        shorterPath = '\\'.join(parts[:i])
        files = self.index_manager.get_indexed_files()

        while i>-len(parts):
            for e in files:
                if e.count(shorterPath)>0 and e.cont(path)==0:
                    return VNode().build(e)
            i = i-1
            shorterPath = os.sep.join(parts[:i])

        return None    
        
    def is_traversable(self, path:str):
        return len([i for i in self.index_manager.get_indexed_files() if i.count(path)>0 and len(i)>len(path)])>0