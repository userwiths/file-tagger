from tkinter import  *

class Grid(Frame):
    def __init__(self, parent,perRow:int):
        Frame.__init__(self, parent)
        self.items=[]
        self.perRow=perRow

    def add(self,item):
        position=self.__next_position()
        item.grid(row=position[0],column=position[1])
        self.items.append(item)

    def clear(self):
        pass

    def __next_position(self):
        counter=len(self.items)
        return (int(counter/self.perRow),int(counter%self.perRow))
         
    def redraw(self):
        counter=1
        row_number=0
        column=0
        currentFrame=self

        for row in self.rows:
            column=int(counter%self.perRow)
            row.grid(row=row_number,column=column)

            if counter%self.perRow==0:
                row_number+=1
            counter+=1

        self.rows.append(currentFrame)