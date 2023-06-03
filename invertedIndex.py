from pathlib import Path
import json
import os
import re
from nltk.stem import PorterStemmer

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
   
    #Clears the inverted index
    def clear_token_map(self):
        self.token_map.clear()

#Starts the program
if __name__ == '__main__':
    #Create a blank inverted index
    invertedTokenIndex = InvertedIndex()
    #Create a dictionary which holds the docIDs with their associated URLs
    docIndex = dict()
    #Store unique tokens
    unique_tokens = set()

    #Path to the Dev file provided by professor.
    devDirect = '/home/jayl9/elasticsearch/DEV'
    docid = 0
    index_size = 0
    for subdirectories in Path(devDirect).iterdir():
        if subdirectories.is_dir():
            for file in Path(subdirectories).iterdir():

                if((docid % 5000 == 0) and (docid != 0)):
                    #Transfer to the tokenfile
                    invertedfilename = "m1invertedindex" + str(docid) + ".json"
                    with open(invertedfilename, "w") as invertedfile:
                        json.dump(dict(sorted(invertedTokenIndex.get_inverted_index().items())), invertedfile)
                
                    #Dumps the DocIndex into a json file, used for search querying later on
                    docindexfilename = "m1docindex" + str(docid) + ".json"
                    with open(docindexfilename, "w") as docindexfile:
                        json.dump(docIndex, docindexfile)
                        
                    # Update the index size
                    index_size += os.path.getsize(invertedfilename)
                    index_size += os.path.getsize(docindexfilename)

                    #Wipe the invertedTokenIndex & Doc index
                    invertedTokenIndex.clear_token_map()
                    docIndex.clear()
                    

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
                
                #create a porter stemmer object
                ps = PorterStemmer()

                #set for all the important tokens
                important_words = set()

                #list of important tags
                important_tags = ['h1','h2','h3','strong','b','title']

                #loop through all the tags
                for tag in important_tags:
                    #loop through all elements of that tag
                    for element in soup.find_all(tag):
                        #convert it to a string
                        important_string = element.string
                        #check if string is not none
                        if important_string is not None:
                            #convert string into a list of lower case words
                            important_string_list = important_string.lower().split()
                            #loop through all the words in the list
                            for word in important_string_list:
                                #stem the word
                                stemmed_word = ps.stem(word)
                                #add the stemmed word into the set of important words
                                important_words.add(stemmed_word)
                
                #Puts the stemmed tokens from the list into the temp dictionary with frequencies
                for token in lowerTokenList:
                    stemmed_token = ps.stem(token)
                    unique_tokens.add(stemmed_token)
                    if stemmed_token not in tempTokenDictionary:
                        tempTokenDictionary[stemmed_token] = 1
                    else:
                        tempTokenDictionary[stemmed_token] += 1

                #Add the postings to the inverted index
                for token, frequency in tempTokenDictionary.items():
                    isImportant = 0
                    if token in important_words:
                        isImportant = 1
                    posting = (docid, frequency, isImportant)
                    invertedTokenIndex.add_document(token, posting)

                #Closes the file
                jsonfile.close()
    
    #Prints how many docs we went through (testing only, delete later)
    print("1. Number of indexed Documents:  " + str(docid))
    #Prints how many unique words there are (M1 only, delete later)
    print("2. Number of unique words:  " + str(len(unique_tokens)))
    index_size_kb = index_size / 1024
    print("3. Total index size on disk: {:.2f} KB".format(index_size_kb))

    #Dumps the InvertedIndex into a json file, used for search querying and storage later on.
    with open("m1invertedindexEnd.json", "w") as invertedfile:
        json.dump(dict(sorted(invertedTokenIndex.get_inverted_index().items())), invertedfile)
    
    #Dumps the DocIndex into a json file, used for search querying later on
    with open("m1docindex.json", "w") as docindexfile:
        json.dump(docIndex, docindexfile)
