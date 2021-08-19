import csv
import sympy
from declaration import config, factory, invalidate

class IndexManager:
    def __init__(self):
        self.index_item_file=config.indexFile
        self.indexed_items=[]

        self.delimiter=';'
        self.new_line=''
    
    def get_indexed_files(self):
        """
        Returns all currently tagged files.
        """
        self.indexed_items=[]
        path=self.index_item_file

        with open(path,newline=self.new_line) as csvfile:
            reader=csv.reader(csvfile,delimiter=self.delimiter)
            for row in reader:
                if len(row)>=2:
                    self.indexed_items.append(row)

        return self.indexed_items

    @invalidate
    def tag_item(self,tag_number:int,item_path:str):
        """
        Tag a file identified by 'item_path' with the 'tag_number' that represents the collection of tags.
        """
        if self.is_tagged(item_path):
            self.edit_tag(tag_indexes,item_path)
            return

        with open(self.index_item_file, 'a', newline=self.new_line) as f:
            writer = csv.writer(f,delimiter=self.delimiter)
            writer.writerow([item_path,tag_number,self.get_type(item_path)])
        
    @invalidate
    def edit_tag(self,tag_number:int,item_path:str):
        """
        Change tag number of a given item.
        """
        files_indexes=self.indexed_items
        
        with open(self.index_item_file, 'w', newline=self.new_line) as f:
            writer = csv.writer(f,delimiter=self.delimiter)
            for index in files_indexes:        
                if index[0]==item_path:
                    writer.writerow([item_path,tag_number,self.get_type(item_path)])
                else:
                    writer.writerow(index)

    def get_items_with_all_tags(self,number:int):
        """
        Returns a list of the items containing ALL tags defined by 'number'
        """
        return [i[0] for i in self.indexed_items if i[1].strip('\n').endswith(str(number))]

    def get_items_with_any_tag(self,numbers:list):
        """
        Returns a list of items tagged with ANY of the tags in 'numbers'
        """
        result=[]
        for item in self.indexed_items:
            number=int(item[1].strip('\n'))
            for index in numbers:
                if number%index==0:
                    result.append(item)
                    break

        return result

    def is_tagged(self,item:str):
        """
        Returns 'true' in case the 'item' has been tagged with any tag.
        """
        return len([i for i in self.indexed_items if i[1].strip('\n')==item])>0

    def reindex_files(self,removed_tag_number:int):
        """
        Reindex in case a tag has been deleted.
        """
        files_indexes=self.indexed_items
        number=0
        with open(self.index_item_file, 'w', newline=self.new_line) as f:
            writer = csv.writer(f,delimiter=self.delimiter)
            writer.writerow([index[0],str(number),index[2]])

    def get_type(self,path):
        if path.startswith("http"):
            return "http"
        else:
            return "filesystem"