from pathlib import Path
import zipfile
import json
import os
import re

from bs4 import BeautifulSoup

class InvertedIndex:
    #Token: [Postings]
    token_map = dict()

    def add_document(self, doc_name, tokens): #Add document name/id to the list of documents
        pass
    def get_posting(self, term): #return a posting list for a given term
        pass
    def get_document_frequency(self, term): #return document frequency 
        pass
    #Don't do for M1
    def check_tfidf(self, doc_name, term): #check the tf-idf score
        pass

#Class that holds a DocID & associated frequency.
class Posting:
    def __init__(self, docid, frequency):
        self.docid = docid
        self.frequency = frequency
    #Returns ID
    def getid(self):
        return self.docid
    #Returns Frequency
    def getFrequency(self):
        return self.frequency


#TO DO LATER:
#Create a dictionary that holds the docID (int) with their associated url (string).



#Starts the program
if __name__ == '__main__':
    #Create a blank inverted index
    invertedTokenIndex = InvertedIndex()

    #Path to the Dev file provided by professor.
    devDirect = '/home/vanoverc/INF141/Assignment3/elasticsearch/DEV'
    fileCounter = 0
    docid = 0
    for subdirectories in Path(devDirect).iterdir():
        if subdirectories.is_dir():
            for file in Path(subdirectories).iterdir():
                jsonfile = open(file, "r")
                fileCounter += 1
                jsonData = json.load(jsonfile)
                """#Parse through the body content/ content within the json file
                soup = BeautifulSoup(jsonData["content"], 'html.parser')
                bodyContent = soup.get_text()


                #Tokenize the bodyContent here
                updated_text_string = re.findall("[^a-zA-Z0-9']", " ", bodyContent)
                tokens = updated_text_string.split()"""
                


    # for devDirect, subdirectories, devFiles in os.walk(devDirect):
    #     #Inner for loop which goes through each subdirectory in Dev file
    #     for jsonFile in subdirectories:
    #         for devDirect2, subdirectories2, devFiles2 in os.walk(os.path.join(devDirect, jsonFile)):
    #             #Load the json file into a dictionary object using json import
    #             for actualFile in subdirectories2:
    #                 print(actualFile)
                    # file = open(actualFile, "r")
                    # jsonData = json.load(file)
                    # fileCounter += 1


                    #     #Parse through the content within the json file
                    #     #soup = BeautifulSoup(jsonData["content"], 'html.parser')
                    #     #bodyContent = soup.get_text()

                    # print("File could not be opened or does not exist") 


            #Parse through the bodyContent here

            #Tokenize the bodyContent here

            #Create Posting objects. Add them to the invertedIndex object

            #Add to the dictionary that holds docID & url name


            #End of dealing with this class object
    print(fileCounter)

#Zip -> folder -> json files
#Zip -> json files
#git test
#git test 2 