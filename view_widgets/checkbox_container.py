from tkinter import  *

class CheckBoxContainer(Frame):
    def __init__(self, parent=None, keys=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.rows=[]
        self.values = []
        self.config={
            "grid":False,
            "side":LEFT,
            "anchor":W,
            "expand":YES,
            "perRow":3
        }
        self.generateContainer(keys,side,anchor)
         
    def generateContainer(self,keys=[],side=LEFT, anchor=W):
        counter=1
        row=0
        column=0
        currentFrame=self

        for key in keys:
            column=int(counter%self.config["perRow"])
            value = IntVar()
            chk = Checkbutton(self, text=key, variable=value)
            chk.grid(row=row,column=column)
            self.values.append((key,value))

            if counter%self.config["perRow"]==0:
                row+=1
            counter+=1

        self.rows.append(currentFrame)

    def getValues(self):
        return [i[1] for i in self.values]

    def getKeys(self):
        return [i[0] for i in self.values]

    def getSelected(self):
        return [i for i in self.values if i[0]!=0]