from core import config, factory

class IndexManager:
    def __init__(self):
        self.index_item_file=config.indexFile
        
    # Use and override for new implementations 
    def get_indexed_files(self):
        file=open(self.index_item_file,"r")
        lines=file.readlines()
        file.close()

        return lines
    
    def tag_item(self,tag_number,item_path):
        if self.is_tagged(item_path):
            self.edit_tag(tag_indexes,item_path)
            return

        file=open(self.index_item_file,"a")
        file.write(item_path+";"+str(tag_number)+'\n')
        file.close()

    
    def edit_tag(self,tag_indexes,item_path):
        pass

    def get_items_with_all_tags(self,number):
        return [i.split(';')[0] for i in self.get_indexed_files() if i.strip('\n').endswith(str(number))]

    def get_items_with_any_tag(self,numbers):
        result=[]
        for item in self.get_indexed_files():
            number=int(item.strip('\n').split(';')[1])
            for index in numbers:
                if number%index==0:
                    result.append(item)
                    break

        return result

    def is_tagged(self,item):
        return len([i for i in self.get_indexed_files() if i.strip('\n')==item])>0

    def reindex_files(self,removed_tag_number):
        files_indexes=self.get_indexed_files()
        number=0
        file=open(self.index_item_file,'w')
        for index in files_indexes:
            number=int(index.split(';')[1])/removed_tag_number
            file.write(index.split(';')[0]+";"+str(number)+'\n')
        file.close()