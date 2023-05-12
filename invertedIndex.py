from pathlib import Path
import zipfile
import json
import os
import re

from bs4 import BeautifulSoup

class InvertedIndex:
    #Token: [Postings]
    #In depth Example:
    #{Token: [Posting DocA, Posting DocB, Posting DocC], Token2: [etc.]}
    token_map = dict()

    def get_inverted_index(self): #Returns the InvertedIndex as a dictionary object 
        return self.token_map
    
    def add_document(self, token, posting): #Add document name/id to the list of documents
        if token in self.token_map:
            self.token_map[token].append(posting)
        else:
            self.token_map[token] = [posting]

    def get_posting(self, term): #return a posting list for a given term
        if term in self.token_map:
            return self.token_map[term]
        
    def get_highest_token_frequency(self, term): #return document frequency 
        highestFreq = 0
        doc = -1
        #Checks if the term is in the dictionary, if so, returns the docID of the one with the highest frequency.
        if term not in self.token_map:
            print("There is no documents associated with that token")
            return doc
        else:
            for eachPosting in self.token_map[term]:
                if eachPosting.getFrequency() > highestFreq:
                    highestFreq = eachPosting[1]
                    doc = eachPosting[0]
            return doc
        
    def get_total_tokens(self): #Returns the number of tokens in the inverted index
        return len(self.token_map)

    #Don't do for M1
    def check_tfidf(self, doc_name, term): #check the tf-idf score
        pass

"""
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
"""



#Starts the program
if __name__ == '__main__':
    #Create a blank inverted index
    invertedTokenIndex = InvertedIndex()
    #Create a dictionary which holds the docIDs with their associated URLs
    docIndex = dict()

    #Path to the Dev file provided by professor.
    devDirect = '/home/vanoverc/INF141/Assignment3/elasticsearch/DEV'
    docid = 0
    for subdirectories in Path(devDirect).iterdir():
        if subdirectories.is_dir():
            for file in Path(subdirectories).iterdir():

                if((docid % 5000 == 0) and (docid != 0)):
                    #Transfer to the tokenfile
                    with open("m1invertedindex" + str(docid) + ".json" , "w") as invertedfile:
                        json.dump(invertedTokenIndex.get_inverted_index(), invertedfile)
                
                    #Dumps the DocIndex into a json file, used for search querying later on
                    with open("m1docindex" + str(docid) + ".json", "w") as docindexfile:
                        json.dump(docIndex, docindexfile)

                    #Wipe the invertedTokenIndex & Doc index
                    invertedTokenIndex = InvertedIndex()
                    docIndex = dict()

                jsonfile = open(file, "r")
                #Updates the DocID for a new file
                docid += 1
                print(file)

                #Loads the JSON data into a dictionary object
                jsonData = json.load(jsonfile)

                #Adds the url with its associated docID to the urlDictionary
                docIndex[docid] = jsonData["url"]

                #Parse through the body content/ content within the json dictionary data
                soup = BeautifulSoup(jsonData["content"], 'html.parser')
                #Raw String of content from json file.
                bodyContent = soup.get_text()

                #Tokenize the bodyContent here
                updatedTextString = re.sub("[^a-zA-Z0-9]", " ", bodyContent)
                #Splits text string to get rid of white space between words. Result is a list of words
                tokenList = updatedTextString.split()
                #Converts all to lowercase for tokenization
                lowerTokenList = [eachIndex.lower() for eachIndex in tokenList]

                #Creates a temporary dictionary for holding frequency of each token, will be used to create postings later.
                tempTokenDictionary = dict()

                #Puts the tokens from the list into the temp dictionary with frequencies
                for token in lowerTokenList:
                    if token not in tempTokenDictionary:
                        tempTokenDictionary[token] = 1
                    else:
                        tempTokenDictionary[token] += 1

                #Add the postings to the inverted index
                for token, frequency in tempTokenDictionary.items():
                    posting = (docid, frequency)
                    invertedTokenIndex.add_document(token, posting)

                #Closes the file
                jsonfile.close()
    
    #Prints how many docs we went through (testing only, delete later)
    print("1. Number of indexed Documents:  " + str(docid))
    #Prints how many unique words there are (M1 only, delete later)
    print("2. Number of unique words:  " + str(invertedTokenIndex.get_total_tokens()))

    #Dumps the InvertedIndex into a json file, used for search querying and storage later on.
    with open("m1invertedindexEnd.json", "w") as invertedfile:
        json.dump(invertedTokenIndex.get_inverted_index(), invertedfile)
    
    #Dumps the DocIndex into a json file, used for search querying later on
    with open("m1docindex.json", "w") as docindexfile:
        json.dump(docIndex, docindexfile)

#Zip -> folder -> json files
#Zip -> json files
#git test
#git test 2 