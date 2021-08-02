import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import uuid,os, sys,subprocess
import sympy,re

from index import IndexManager
from tags import TagManager
from view_widgets import TreeManager

class Factory:
    def __init__(self):
        # {NAME:INSTANCE}
        self.register=[]

    def setInstance(obj):
        self.register.append({
            'name':obj.__class__,
            'instance':obj
        })

    def getInstance(className):
        for i in self.register:
            if i['name'].__class__==className:
                return i['instance']

class ConfigurationManager:
    def __init__(self):
        self.indexFile='index.txt'
        self.tagsFile='tags.txt'
        self.browseRoot='D:\\Other'

        self.indexManager='IndexManager'
        self.tagsManager='TagManager'
        self.treeManager='TreeManager'

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.indexManager=IndexManager()
        self.tagManager=TagManager(self.indexManager)
        self.notebook=ttk.Notebook(master)
        self.checkBoxes=[]
        self.path='D:/Other'

        self.frame=tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.frameTwo=tk.Frame(master)
        self.frameTwo.pack(fill="both", expand=True)
        self.frameTwo.columnconfigure([i for i in range(1,12)], weight=1, minsize=20)
        self.frameTwo.rowconfigure([i for i in range(1,12)], weight=1, minsize=20)

        self.tagManagementFrame=tk.Frame(master)
        self.tagManagementFrame.pack(fill="both", expand=True)

        self.checkboxFrame=tk.Frame(self.frame)
        self.checkboxFrame.grid(column=2,columnspan=6,row=2)
        self.addCheckboxes()

        abspath = os.path.abspath(self.path)
        self.tree = TreeManager(self,self.frame,self.tagManager,self.indexManager,abspath,"File Browser",self.process_directory)

        self.treeIndexed = TreeManager(self,self.frameTwo,self.tagManager,self.indexManager,'Index',"Indexed Files",self.process_indexed_directory)
        self.treeIndexed.bind("<Double-1>", self.indexedDoubleClick)

        self.tagName=tk.Entry(self.tagManagementFrame)
        self.tagList=self.addListBox()
        self.editTag=tk.Button(self.tagManagementFrame,text="Apply",command=self.apply_tag_action)
        
        self.tagName.pack()
        self.editTag.pack()
        self.tagList.pack()

        self.headerAndFooter()
        self.loadTabs([{'frame':self.frame,'text':'File Tagger'},{'frame':self.frameTwo,'text':'Indexed Files'},{'frame':self.tagManagementFrame,'text':'Manage Tags'}])

        self.tree.drawTree()
        self.treeIndexed.drawTree()

    def loadTabs(self,tabs_data):
        for tab in tabs_data:
            self.notebook.add(tab['frame'],text=tab['text'])
        self.notebook.pack()
        
    def headerAndFooter(self):
        self.header=tk.Frame(self.master)
        self.header.pack(side="top")

        self.buttonFrame=tk.Frame(self.master)
        self.buttonFrame.pack(side="bottom")
        self.addButtons()

    def indexedDoubleClick(self,event):
        item=self.treeIndexed.selection()[0]
        path=[self.treeIndexed.item(item)['text']]
        while self.treeIndexed.parent(item):
            item=self.treeIndexed.parent(item)
            path.insert(0,self.treeIndexed.item(item)['text'])
        path.remove(path[0])
        print('\\'.join(path))
        try:
            retcode = subprocess.call("start " + '\\'.join(path), shell=True)
            if retcode < 0:
                print("Child was terminated by signal "+ str(-retcode))
            else:
                print("Child returned "+ str(retcode))
        except OSError:
            print("Execution failed:")

    def addListBox(self):
        box=tk.Listbox(self.tagManagementFrame)
        counter=1

        box.insert(0, '(Create New Tag)')  
        for tag in self.tagManager.get_tags():
            box.insert(counter, tag)  
            counter+=1

        return box

    def addDropBox(self):
        pass

    def addButtons(self):
        quit = tk.Button(self.buttonFrame, text="QUIT",command=self.master.destroy)
        quit.grid(row=6,column=2)
        openfile = tk.Button(self.buttonFrame, text="FILE",command=self.select_file)
        openfile.grid(row=6,column=4)
        opendir = tk.Button(self.buttonFrame, text="DIRECTORY",command=self.select_directory)
        opendir.grid(row=6,column=6)
        opendir = tk.Button(self.buttonFrame, text="TAG",command=self.tag_item)
        opendir.grid(row=6,column=8)

    def tag_item(self):
        self.tagManager.tag_item([1,2],self.tree.get_path(self.tree.selection(),False))

    def addCheckboxes(self):
        index=0
        nrow=0
        ncol=0
        checkbox=None
        label=None
        for i in self.tagManager.get_tags():
            if index%3==0:
                nrow=0
                ncol=ncol+1
            asd=int()             
            checkbox=tk.Checkbutton(self.checkboxFrame, variable = asd)
            self.checkBoxes.append(asd)
            label=tk.Label(self.checkboxFrame,text=str(i))
            
            label.grid(row=nrow,column=ncol)
            checkbox.grid(row=nrow,column=ncol+1)

            nrow+=1
            index+=1

    def addCombobox(self):
        pass

    def select_directory(self):
        result=fd.askdirectory()
        self.path=result

    def select_file(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        self.path=filename

    def process_indexed_directory(self, parent, path):
        items=[file.split(';')[0] for file in self.tagManager.indexManager.get_indexed_files()]
        formated_file=[]
        map=[]
        branch=parent
        for file in items:
            formated_file=re.split(r' |/|\\',file)
            
            for part in formated_file:
                same_name=[e for e in map if e[1]==part]
                if len([child for child in self.treeIndexed.get_children(branch) if self.treeIndexed.item(child)['text']==part])==0:
                    branch=self.treeIndexed.insert(branch, 'end', text=part, open=False)
                    map.append((branch,part))
                else:
                    branch=[e[0] for e in map if e[1]==part][0]
            branch=parent

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.tree.insert(oid, 'end', text='', open=False)
    
    def open_directory_tree(self,event):
        if event.widget.heading('#0')['text']=="Indexed Files":
            return

        selected_id=self.tree.selection()
        selected_item=self.tree.item(selected_id)
        children=self.tree.get_children(selected_id)
        for i in children:
            self.tree.delete(i)
        self.process_directory(selected_id,self.tree.get_path(selected_id,False))

    def close_directory_tree(self,event):
        if event.widget.heading('#0')['text']=="Indexed Files":
            return

        selected_id=self.tree.focus()
        selected_item=self.tree.item(selected_id)
        for i in self.tree.get_children(selected_id):
            self.tree.delete(i)
        self.tree.insert(selected_id,'end',text='',open=False)
    
    def apply_tag_action(self):
        selectedIndex=self.tagList.curselection()[0]
        print(selectedIndex)
        if selectedIndex==0 :
            self.tagManager.add_new_tag(self.tagName.get())
        else:
            self.tagManager.edit_existing_tag(selectedIndex-1,self.tagName.get())

    

if __name__=="__main__":
    root=tk.Tk()
    app=Application(root)
    
    root.bind('<<TreeviewOpen>>',app.open_directory_tree)
    root.bind('<<TreeviewClose>>',app.close_directory_tree)

    app.mainloop()