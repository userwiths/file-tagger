import csv
import sympy
from core import TagManager
from declaration import config, factory, invalidate

class TagManager(TagManager):
    def __init__(self):
        self.indexManager=factory.getInstanceByName(config.indexManager)
        self.tags_file=config.tagsFile
        self.tags=[]
        self.available_tags=[]
        self.selected_paths=[]

        self.delimiter=';'

    # Use and override for new implementations 
    def get_tags(self):
        if len(self.available_tags)==0:
            self.load_tags()

        return self.available_tags
    
    def load_tags(self):
        self.tags=[]
        path=self.tags_file

        with open(path,newline='') as csvfile:
            reader=csv.reader(csvfile,delimiter=self.delimiter)
            for row in reader:
                if len(row)==2:
                    self.tags.append(row)
                    self.available_tags.append(row[1])

        return self.tags
        
    #Get number coresponding to a unique sequence of tags.
    def calc_tags_number(self,tag_indexes:list):
        number=1
        for i in range(0,len(tag_indexes)):
            if(tag_indexes[i]!=0):
                number*=int(self.tags[i][0])
        return number

    #Get unique sequence of tags coresponding to a given number.
    def calc_number_tags(self,number:int):
        return [i for i in sympy.divisors(number) if sympy.isprime(i)]

    def get_tag_number(self,tag_index:int):
        return int(self.tags[tag_index][0])

    def get_tag_index_text(self,tag_index:int):
        return self.tags[tag_index][1]

    def get_tag_value_text(self,tag_value:int):
        return [i[1] for i in self.tags if int(i[0])==tag_value][0]

    def get_number_item(self,item_path:str):
        return [i.split(';')[1] for i in self.get_indexed_files() if i.strip('\n')==item_path]

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

    @invalidate
    def add_new_tag(self,tag_name:str):
        #get last assigned number
        number=int(self.tags[-1][0])
        number=sympy.nextprime(number)

        with open(self.tags_file, 'a', newline='') as f:
            writer = csv.writer(f,delimiter=self.delimiter)
            writer.writerow([number,tag_name])
        
        self.load_tags()

        return number


    @invalidate
    def remove_existing_tag(self,tag_index:int):
        value_remove=int(self.tags[tag_index][0])
        self.indexManager.reindex_files(value_remove)
        tags=[]
        with open(self.tags_file,newline='') as csvfile:
            reader=csv.reader(csvfile,delimiter=self.delimiter)
            for row in reader:
                if int(row[0])!=value_remove:
                    tags.append(row)

        with open(self.tags_file, 'w', newline='') as f:
            writer = csv.writer(f,delimiter=self.delimiter)
            writer.writerows(tags)

    @invalidate
    def edit_existing_tag(self,tag_index:int,tag_name:str):
        tags=[]
        edited_tag=self.tags[tag_index]
        
        with open(self.tags_file,newline='') as csvfile:
            reader=csv.reader(csvfile,delimiter=self.delimiter)
            for row in reader:
                if row[0]==edited_tag[0]:
                    tags.append([row[0],tag_name])
                else:
                    tags.append(row)

        with open(self.tags_file, 'a', newline='') as f:
            writer = csv.writer(f,delimiter=self.delimiter)
            writer.writerows(tags)