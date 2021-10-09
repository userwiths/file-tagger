from tkinter import  *

class Grid(Frame):
    def __init__(self, parent,perRow:int):
        Frame.__init__(self, parent)
        self.config={
            "perRow":perRow,
            "items":{
                "row_span":1,
                "column_span":1
            }
        }
        self.items=[]

    def add(self,item):
        position=self.__next_position()
        item.grid(
            row=position[0],
            column=position[1],
            rowspan=self.config["items"]["row_span"],
            columnspan=self.config["items"]["column_span"]
        )
        self.items.append(item)

    def clear(self):
        pass

    def __next_position(self):
        perRow=rowspan=self.config["perRow"]
        counter=len(self.items)
        return (int(counter/perRow),int(counter%perRow))
         
    def redraw(self):
        perRow=rowspan=self.config["perRow"]
        counter=1
        row_number=0
        column=0
        currentFrame=self

        for row in self.rows:
            column=int(counter%perRow)
            row.grid(row=row_number,column=column)

            if counter%perRow==0:
                row_number+=1
            counter+=1

        self.rows.append(currentFrame)