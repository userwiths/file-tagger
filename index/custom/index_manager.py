from declaration import config, factory

class IndexManager:
    def __init__(self):
        self.index_item_file=config.indexFile
        
    # Use and override for new implementations 
    def get_indexed_files(self):
        """
        Load indexed files in memory.
        """
        file=open(self.index_item_file,"r")
        lines=file.readlines()
        file.close()

        return lines
    
    def tag_item(self,tag_number:int,item_path:str):
        """
        Tag a file identified by 'item_path' with the 'tag_number' that represents the collection of tags.
        """
        if self.is_tagged(item_path):
            self.edit_tag(tag_indexes,item_path)
            return

        file=open(self.index_item_file,"a")
        file.write(item_path+";"+str(tag_number)+'\n')
        file.close()

    
    def edit_tag(self,tag_indexes:list,item_path:str):
        pass

    def get_items_with_all_tags(self,number:int):
        """
        Returns a list of the items containing ALL tags defined by 'number'
        """
        return [i.split(';')[0] for i in self.get_indexed_files() if i.strip('\n').endswith(str(number))]

    def get_items_with_any_tag(self,numbers:list):
        """
        Returns a list of items tagged with ANY of the tags in 'numbers'
        """
        result=[]
        for item in self.get_indexed_files():
            number=int(item.strip('\n').split(';')[1])
            for index in numbers:
                if number%index==0:
                    result.append(item)
                    break

        return result

    def is_tagged(self,item:str):
        """
        Returns 'true' in case the 'item' has been tagged with any tag.
        """
        return len([i for i in self.get_indexed_files() if i.strip('\n')==item])>0

    def reindex_files(self,removed_tag_number:int):
        """
        Reindex in case a tag has been deleted.
        """
        files_indexes=self.get_indexed_files()
        number=0
        file=open(self.index_item_file,'w')
        for index in files_indexes:
            number=int(index.split(';')[1])/removed_tag_number
            file.write(index.split(';')[0]+";"+str(number)+'\n')
        file.close()