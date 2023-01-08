from tkinter import *
import tkinter.ttk as ttk;

class Scroller:
    def __init__(self, parentContainer):
        #Frame.__init__(self,parentContainer)
        self.yscroller = ttk.Scrollbar(parentContainer, orient="vertical", command=self.yview)
        self.xscroller = ttk.Scrollbar(parentContainer, orient="horizontal", command=self.xview)
        self.configure(yscroll=self.yscroller.set, xscroll=self.xscroller.set)
        self.yscroller.grid(column=1, row=0, rowspan=10, sticky="ns")
        self.xscroller.grid(column=0, row=10, columnspan=1, sticky="ew")
        self.parentContainer = parentContainer


    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/scrollbar-callback.html