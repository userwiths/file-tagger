import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from view_widgets import TreeManager,BrowserManager,CheckBoxContainer
from declaration import config, factory
from cache import CacheManager

import uuid
import os
import sys
import subprocess
import re
import logging

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        logging.debug('Application Init')
        self.factory = factory
        self.cacheManager = factory.create('cache','CacheManager')
        self.indexManager = factory.create(*config.index)
        self.tagManager = factory.create(*config.tags)
        self.fileManager = factory.create(*config.realFiles)
        self.virtualManager = factory.create(*config.virtualFiles)
        self.fileHandler = factory.create(*config.fileHandler)
        logging.debug('Loaded factory objects from config.')

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=1)
        self.checkBoxes = []
        self.path = '/'

        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.indexedFrame = tk.Frame(master)
        self.indexedFrame.pack(fill=tk.BOTH, expand=True)
        
        self.frameThree = tk.Frame(master)
        self.frameThree.pack(fill=tk.BOTH, expand=True)
        
        self.tagManagementFrame = tk.Frame(master)
        self.tagManagementFrame.pack(fill=tk.BOTH, expand=True)

        self.checkboxFrame = CheckBoxContainer(self.frame, self.tagManager.get_tags())#tk.Frame(self.frame)
        self.checkboxFrame.grid(rowspan=4, column=2, columnspan=6, row=2)
        #self.addCheckboxes()

        self.tree = TreeManager(self, self.frame, os.path.abspath(self.path), "filesystem", self.process_directory)

        self.browserIndexed = BrowserManager(self,self.indexedFrame, ['filesystem',"http"], "Indexed Files", self.browser_directory_process)
        self.browserIndexed.bind("<Double-1>", self.indexedDoubleClick)

        self.tagName=tk.Entry(self.tagManagementFrame)
        self.tagList=self.addListBox()
        self.editTag=tk.Button(self.tagManagementFrame,text="Apply",command=self.apply_tag_action)
        
        self.tagName.pack()
        self.editTag.pack()
        self.tagList.pack()

        self.headerAndFooter()
        self.loadTabs([{'frame':self.frame,'text':'File Tagger'},{'frame':self.indexedFrame,'text':'Indexed Files'},{'frame':self.tagManagementFrame,'text':'Manage Tags'}])

        self.tree.drawTree()
        self.browserIndexed.drawTree()
        logging.debug("Finished UI Loading")

    def loadTabs(self, tabs_data:dict):
        for tab in tabs_data:
            self.notebook.add(tab['frame'],text=tab['text'])
        self.notebook.pack(expand=True)
        
    def headerAndFooter(self):
        self.header = tk.Frame(self.master)
        self.header.pack(side="top")

        self.buttonFrame = tk.Frame(self.master)
        self.buttonFrame.pack(side="bottom")
        self.addButtons()

    def indexedDoubleClick(self, event):
        item = self.browserIndexed.selection()[0]
        path = self.browserIndexed.get_path(item,True)
        logging.debug("Double clicked on " + item + " pointing towards " + path)
        self.fileHandler.handle(path)

    def addListBox(self):
        box = tk.Listbox(self.tagManagementFrame)
        counter = 1
        box.insert(0, '(Create New Tag)')  
        for tag in self.tagManager.get_tags():
            box.insert(counter, tag)  
            counter += 1

        return box

    def addDropBox(self):
        pass

    def addButtons(self):
        quit = tk.Button(self.buttonFrame, text="QUIT", command=self.master.destroy)
        quit.grid(row=6, column=2)
        openfile = tk.Button(self.buttonFrame, text="FILE", command=self.select_file)
        openfile.grid(row=6, column=4)
        opendir = tk.Button(self.buttonFrame, text="DIRECTORY", command=self.select_directory)
        opendir.grid(row=6, column=6)
        opendir = tk.Button(self.buttonFrame, text="TAG", command=self.tag_item)
        opendir.grid(row=6, column=8)

    def tag_item(self):
        logging.debug("Tagging item : " + self.tree.get_path(self.tree.selection(), False))
        self.indexManager.tag_item(self.tagManager.calc_tags_number([i.get() for i in self.checkboxFrame.getValues()]), self.tree.get_path(self.tree.selection(), False))

    def addCheckboxes(self):
        index = 0
        nrow = 0
        ncol = 0
        checkbox = None
        label = None
        for i in self.tagManager.get_tags():
            if index%3==0:
                nrow = 0
                ncol = ncol+1

            value = tk.IntVar()             
            checkbox = tk.Checkbutton(self.checkboxFrame, variable = value)
            self.checkBoxes.append(value)
            label = tk.Label(self.checkboxFrame, text=str(i))
            
            label.grid(row=nrow, column=ncol)
            checkbox.grid(row=nrow, column=ncol+2)

            nrow += 2
            index += 1

    def addCombobox(self):
        pass

    def select_directory(self):
        result = fd.askdirectory()
        self.path = result

    def select_file(self):
        filetypes = (
            ('Text files', '*.txt'),
            ('All files', '*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )

        self.path = filename

    def browser_directory_process(self, path:str):
        vnodes = self.virtualManager.get_all_items()
        formated_file = []
        map = []
        logging.debug("Opening " + path)
        for file in vnodes:
            branch = [i for i in self.browserIndexed.get_children() if self.browserIndexed.item(i)['text']==file.other[0]]

            currentPath = file.path
            value = file.value
            formated_file = re.split(r' |/|\\', currentPath)
            
            for part in formated_file:
                if not file.path.endswith(part):
                    value = None
                else:
                    value = int(file.value)
                    index_arr = self.tagManager.calc_number_tags(value)
                    text_tags = [self.tagManager.get_tag_value_text(i) for i in index_arr]
                    value = ",".join(text_tags)
                    
                same_name = [e for e in map if e[1]==part]
                if len([child for child in self.browserIndexed.get_children(branch) if self.browserIndexed.item(child)['text']==part])==0:
                    branch = self.browserIndexed.insert(branch, 'end', text=part, value=(file.name,value), open=False)
                    map.append((branch,part))
                else:
                    branch=[e[0] for e in map if e[1]==part][0]

    def process_directory(self, parent, path):
        for p in self.fileManager.get_children(path):
            abspath = os.path.join(path, p)
            isdir = self.fileManager.is_traversable(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.tree.insert(oid, 'end', text='', open=False)
    
    def open_directory_tree(self,event):
        if event.widget.heading('#0')['text'] != "filesystem":
            return
        selected_id = self.tree.selection()
        selected_item = self.tree.item(selected_id)
        children = self.tree.get_children(selected_id)
        for i in children:
            self.tree.delete(i)
        self.process_directory(selected_id, self.tree.get_path(selected_id, False))

    def close_directory_tree(self, event):
        if event.widget.heading('#0')['text']=="filesystem":
            return

        selected_id = self.tree.focus()
        selected_item = self.tree.item(selected_id)
        for i in self.tree.get_children(selected_id):
            self.tree.delete(i)
        self.tree.insert(selected_id, 'end', text='', open=False)
    
    def apply_tag_action(self):
        selectedIndex = self.tagList.curselection()[0]
        if selectedIndex==0 :
            self.tagManager.add_new_tag(self.tagName.get())
        elif self.tagName.get() == "":
            self.tagManager.remove_existing_tag(selectedIndex-1)
        else:
            self.tagManager.edit_existing_tag(selectedIndex-1, self.tagName.get())

    

if __name__=="__main__":
    root = tk.Tk()
    app = Application(root)
    
    app.master.maxsize(1000,900)
    root.bind('<<TreeviewOpen>>', app.open_directory_tree)
    root.bind('<<TreeviewClose>>', app.close_directory_tree)

    app.mainloop()