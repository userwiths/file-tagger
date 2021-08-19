from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk

from declaration import config, factory

class BrowserManager(ttk.Treeview):
    """
    Represents a tree which is used to display the currently tagged files and theyr tag numbers or/and tags.
    """

    def __init__(self,application,parentContainer,root_nodes,header,populate_tree):
        self.columns=[
            ['name','Name'],
            ['tags','Tags']
        ]
        
        super().__init__(parentContainer,columns=[i[0] for i in self.columns],show='tree',displaycolumns=['tags'])

        for i in self.columns:
            self.heading(i[0],text=i[1])
        self.heading('#0',text='')

        self.indexer=factory.getInstanceByName(config.indexManager)
        self.tagger=factory.getInstanceByName(config.tagsManager)
        self.application=application
        self.rootText=root_nodes[0]

        ysb = ttk.Scrollbar(parentContainer, orient='vertical', command=self.yview)
        xsb = ttk.Scrollbar(parentContainer, orient='horizontal', command=self.xview)
        
        self.configure(yscroll=ysb.set, xscroll=xsb.set)
        
        self.root_nodes=root_nodes
        
        self.__init_childs__()
        
        self.populate_tree=populate_tree

        self.grid(row=0, column=0,rowspan=10)
        ysb.grid(column=1,row=0,rowspan=10,sticky="ns")
        xsb.grid(column=0,row=10,columnspan=1,sticky='ew')

    def __init_childs__(self):
        """
        Creates the basic required child components for the widget.
        """
        skip=True
        self.root_node = self.insert('', 'end', text=self.root_nodes[0], open=True)
        for i in self.root_nodes:
            if skip:
                skip=False
                continue
            self.insert('', 'end', text=i, open=True)

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
        self.__init_childs__()
        self.populate_tree(self.rootText)

    def redrawTree(self):
        pass

    def get_path(self,item,remove_root):
        """
        Get the 'path' to a given item.
        If 'remove_root' is true, remove the value assigned by the root of the tree.
        The path represents the current node's text, prepended by its parent, and so forth untill there is no parent. 
        """
        current_item=self.item(item)
        parent_item=self.parent(item)
        result=[current_item["text"]]
        while parent_item:
            result.insert(0,self.item(parent_item)['text'])
            parent_item=self.parent(parent_item)
        
        if remove_root:
            result.remove(result[0])

        return '\\'.join(result)