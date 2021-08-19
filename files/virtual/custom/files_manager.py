import re
from declaration import config,factory,VNode

class VirtualManager:
    def __init__(self):
        self.index_manager=factory.getInstanceByName(config.indexManager)
        self.tag_manager=factory.getInstanceByName(config.tagsManager)

    def get_root_items(self):
        result=[]
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
        return [VNode().build(i) for i in self.index_manager.get_indexed_files() if VNode().build(i).path==path]

    def get_children(self,path):
        result=[VNode().build(i) for i in self.index_manager.get_indexed_files() if VNode().build(i).path.startswith(path)]
        return [r for r in result if r.path!=path and r.path.startswith(path)]

    def get_parent(self,path):
        files=self.index_manager.get_indexed_files()
        files=[VNode().build(i) for i in files if path.startswith(VNode().build(i).path)]
        return files
        
    def is_traversable(self,path):
        return len([i for i in self.index_manager.get_indexed_files() if VNode().build(i).path.startswith(path) and VNode().build(i).path!=path])>0

    def buildNodeFromLine(self,line):
        vnode=VNode()        
        return vnode.build(line)