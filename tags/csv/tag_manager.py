import csv

class TagManager:
    def __init__(self,indexer):
        self.indexManager=indexer
        self.tags_file="tags.txt"
        self.tags=[]
        self.available_tags=[]
        self.selected_paths=[]

        self.delimiter=';'

    # Use and override for new implementations 
    def get_tags(self):
        if len(self.available_tags)==0:
            self.load_tags()

        return self.available_tags
        
    def load_tags(self,path=''):
        if path=='':
            path=self.tags_file

        with open(path,newline='') as csvfile:
            reader=csv.reader(csvfile,delimiter=self.delimiter)
            for row in reader:
                if len(row)==2:
                    self.tags.append(row)
                    self.available_tags.append(row[1])

        return self.tags

    def tag_item(self,tag_indexes,item_path):
        if self.indexManager.is_tagged(item_path):
            self.edit_tag(tag_indexes,item_path)
            return

        number=self.calc_tags_number(tag_indexes)
        self.indexManager.tag_item(number,item_path)
        
    #Get number coresponding to a unique sequence of tags.
    def calc_tags_number(self,tag_indexes):
        number=1
        for tag in tag_indexes:
            number*=int(self.tags[tag][0])
        return number

    #Get unique sequence of tags coresponding to a given number.
    def calc_number_tags(self,number):
        return [i for i in sympy.divisors(number) if sympy.isprime(i)]

    def get_tag_number(self,tag_index):
        return int(self.tags[tag_index][0])

    def get_number_item(self,item_path):
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

    def add_new_tag(self,tag_name):
        #get last assigned number
        number=int(self.tags[-1][0])
        with open(self.tags_file, 'a', newline='') as f:
            writer = csv.writer(f,delimiter=self.delimiter)
            writer.writerow([number,tag_name])
        return number

    def remove_existing_tag(self,tag_index):
        self.indexManager.reindex_files(int(self.tags[tag_index].split(';')[0]))

    def edit_existing_tag(self,tag_index,tag_name):
        tags=[]
        edited_tag=self.tags[tag_index]
        
        with open(path,newline='') as csvfile:
            reader=csv.reader(csvfile,delimiter=self.delimiter)
            for row in reader:
                if row[0]==edited_tag[0]:
                    tags.append([row[0],tag_name])
                else:
                    tags.append(row)

        with open(self.tags_file, 'a', newline='') as f:
            writer = csv.writer(f,delimiter=self.delimiter)
            writer.writerows(tags)