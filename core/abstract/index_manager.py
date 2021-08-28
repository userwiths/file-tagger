class IndexManager:
    def __init__(self):
        pass

    def get_indexed_files(self):
        pass

    def tag_item(self,tag_number:int,item_path:str):
        pass
        
    def edit_tag(self,tag_number:int,item_path:str):
        pass

    def get_items_with_all_tags(self,number:int):
        pass

    def get_items_with_any_tag(self,numbers:list):
        pass

    def is_tagged(self,item:str):
        pass

    def reindex_files(self,removed_tag_number:int):
        pass

    def get_type(self,path:str):
        pass