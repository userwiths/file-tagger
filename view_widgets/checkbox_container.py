from tkinter import  *
from .abstract import Grid,Scroller

class CheckBoxContainer(Grid,Scroller):
    def __init__(self, parent=None, keys=[], perRow=3):
        Grid.__init__(self, parent,perRow)
        self.values = []
        self.generateContainer(keys)
         
    def generateContainer(self,keys=[]):
        for key in keys:
            value = IntVar()
            chk = Checkbutton(self, text=key, variable=value)
            self.add(chk)
            self.values.append((key,value))

    def getValues(self):
        return [i[1] for i in self.values]

    def getKeys(self):
        return [i[0] for i in self.values]

    def getSelected(self):
        return [i for i in self.values if i[0]!=0]