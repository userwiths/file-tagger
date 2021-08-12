from declartaion import config, factory
from functools import lru_cache

class TagManager:
    def __init__(self):
        self.indexManager=factory.getInstanceByName(config.indexManager)
        self.tags_file=config.tagsFile
        self.tags=[]
        self.available_tags=[]
        self.selected_paths=[]

    # Use and override for new implementations 
    def get_tags(self):
        if len(self.available_tags)==0:
            self.load_tags()

        return self.available_tags
        
    @lru_cache(maxsize=4)
    def load_tags(self):
        path=self.tags_file

        file=open(path,"r")
        tags=file.readlines()
        file.close()

        tempTags=self.format_lines_before_read(tags)
        self.tags=[line.split(';') for line in tempTags]
        self.available_tags=[line[1] for line in self.tags]

        return tags

    def tag_item(self,tag_indexes:list,item_path:str):
        if self.indexManager.is_tagged(item_path):
            self.edit_tag(tag_indexes,item_path)
            return

        number=self.calc_tags_number(tag_indexes)
        self.indexManager.tag_item(number,item_path)
        
    #Get number coresponding to a unique sequence of tags.
    def calc_tags_number(self,tag_indexes:list):
        number=1
        for tag in tag_indexes:
            number*=int(self.tags[tag][0])
        return number

    #Get unique sequence of tags coresponding to a given number.
    def calc_number_tags(self,number:int):
        return [i for i in sympy.divisors(number) if sympy.isprime(i)]

    def get_tags_from(self,number:int):
        tagIndexes=self.calc_number_tags(number)
        result=[]
        for i in tagIndexes:
            result.append(self.available_tags[i])
        return result

    def get_tag_number(self,tag_index:int):
        return int(self.tags[tag_index][0])

    def get_number_item(self,item_path:str):
        return [i.split(';')[1] for i in self.get_indexed_files() if i.strip('\n')==item_path]

    def format_lines_before_read(self,lines:list):
        return [i.strip('\n') for i in lines if not i.startswith(config.commentSymbol) and len(i)>2]

    def verify_tag_integrity(self):
        tags=self.load_tags()
        
        numbers=[]
        names=[]
        
        for tag in tags:
            #unique names
            if names.count(tag[1])>0:
                return False

            #unique numbers
            if numbers.count(tag[0])>0:
                return False 

            #tags are assigned ONLY prime numbers
            if not sympy.isprime(int(tag[0])):
                return False

            names.append(tag[1])
            numbers.append(tag[0])

        return True

    def add_new_tag(self,tag_name:str):
        #get last assigned number
        number=int(self.tags[-1][0])
        #get next prime number to be the assigned to the new tag
        number=sympy.nextprime(number)
        file=open(self.tags_file,'a')
        file.write('\n'+str(number)+";"+tag_name)
        file.close()
        return number

    def remove_existing_tag(self,tag_index:int):
        self.indexManager.reindex_files(int(self.tags[tag_index].split(';')[0]))

    def edit_existing_tag(self,tag_index:int,tag_name:str):
        tags=[]
        edited_tag=self.tags[tag_index]
        file=open(self.tags_file,'r')
        tags=file.readlines()
        file.close()

        file=open(self.tags_file,'w')
        for i in tags:
            if i.count(edited_tag[0]+';'+edited_tag[1])>0:
                file.write(edited_tag[0]+';'+tag_name+'\n')
            else:
                file.write(i)
        file.close()