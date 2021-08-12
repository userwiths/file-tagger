from tkinter import ttk

from declaration import config, factory

class TreeManager(ttk.Treeview):
    """
    Represents a tree which is used to display the silesystem's files and folders.
    """
    def __init__(self,application,parentContainer,root,header,populate_tree):
        super().__init__(parentContainer)

        self.indexer=factory.getInstanceByName(config.indexManager)
        self.tagger=factory.getInstanceByName(config.tagsManager)
        self.application=application
        self.rootText=root

        ysb = ttk.Scrollbar(parentContainer, orient='vertical', command=self.yview)
        xsb = ttk.Scrollbar(parentContainer, orient='horizontal', command=self.xview)
        
        self.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.heading('#0', text=header, anchor='w')

        self.root_text=root
        self.root_node = self.insert('', 'end', text=root, open=True)
        self.populate_tree=populate_tree
        self.grid(row=0, column=0,rowspan=10)
        ysb.grid(column=1,row=0,rowspan=10,sticky="ns")
        xsb.grid(column=0,row=10,columnspan=1,sticky='ew')

    def clear(self):
        """
        Clears all children of the widget.
        """
        self.delete(*self.get_children())

    def drawTree(self):
        """
        Clear the widget and execute the function that is meant to populate it with data.
        """
        self.clear()
        self.root_node = self.insert('', 'end', text=self.root_text, open=True)
        self.populate_tree(self.root_node,self.rootText)

    def redrawTree(self):
        pass

    def get_path(self,item,remove_root):
        current_item=self.item(item)
        parent_item=self.parent(item)
        result=[current_item["text"]]
        while parent_item:
            result.insert(0,self.item(parent_item)['text'])
            parent_item=self.parent(parent_item)
        
        if remove_root:
            result.remove(result[0])

        return '\\'.join(result)