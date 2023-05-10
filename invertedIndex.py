import zipfile
import json
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

    #Runs through the zip file and gets the file info
    with zipfile.ZipFile("developer.zip", "r") as files:
        for fileName in files.namelist():
            #Load the json data into an dict object
            jsonData = json.load(fileName)

            #jsonData = "url", "content", "encoding"
            #Parse through the Content within the json file
            soup = BeautifulSoup(jsonData["content"], 'html.parser')
            bodyContent = soup.get_text()

            #Parse through the bodyContent here

            #Tokenize the bodyContent here

            #Create Posting objects. Add them to the invertedIndex object

            #Add to the dictionary that holds docID & url name


            #End of dealing with this class object
    pass

#Zip -> folder -> json files
#Zip -> json files
#git test