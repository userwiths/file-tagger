from tkinter import *
import tkinter.ttk as ttk;

class Scroller:
    def __init__(self,parentContainer):
        #Frame.__init__(self,parentContainer)
        self.yscroller = ttk.Scrollbar(parentContainer, orient='vertical', command=self.ycommand)
        self.xscroller = ttk.Scrollbar(parentContainer, orient='horizontal', command=self.xcommand)
        self.configure(yscroll=self.yscroller.set, xscroll=self.xscroller.set)
        #Frame.configure(yscrollcommand=ysb.set,xscrollcommand=xsb.set)
        self.yscroller.grid(column=1,row=0,rowspan=10,sticky="ns")
        self.xscroller.grid(column=0,row=10,columnspan=1,sticky='ew')


    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/scrollbar-callback.html
    def ycommand(self,action,value:int,unit=UNITS):
        if isinstance(self,ttk.Treeview):
            self.yview(action,value,unit)
        else:
            pass

    def xcommand(self,action,value:int,unit=UNITS):
        if isinstance(self,ttk.Treeview):
            self.xview(action,value,unit)
        else:
            pass
