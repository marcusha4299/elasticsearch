#Require flask installed "pip install Flask"
from flask import Flask, render_template, request, jsonify

import json
import time
from nltk.stem import PorterStemmer
import math
import re

#create Flask app
app = Flask(__name__)

@app.route('/')

#render HTML template and return respond.
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])

def search():
    #loads the docid index to main memory
    with open('merged_docid_index.json', 'r') as merged_docid_file:
        docid_index = json.load(merged_docid_file)

    #loads the index of index to main memory
    with open('indexofindex.json', 'r') as indexofindex_file:
        index_of_index = json.load(indexofindex_file)

    #opens the inverted index file
    merged_index_file = open('mergedIndex.txt', 'r')

    #start time
    start_time = time.time()

    query_word_string = request.form.get('query')

    #keeps query as alpha numeric string
    query_word_list = re.sub("[^a-zA-Z0-9]", " ", query_word_string).split()

    #list for stemmed query words
    stemmed_query_list = []

    #creates a porter stemmer object
    ps = PorterStemmer()

    #stems all the words in the query and checks if it is in the inverted index,
    #if it is, put in stemmed query list
    for word in query_word_list:
        stemmed_word = ps.stem(word)
        if stemmed_word in index_of_index:
            stemmed_query_list.append(stemmed_word)

    console_output = []
        
    #scenario 1: find queries of length 1
    #check if query is not in the inverted index
    if len(stemmed_query_list) == 0:
        print('No search results for: ' + query_word_list[0])
        console_output.append('No search results for: ' + query_word_list[0])
    #if query is in the inverted index and is length 1
    elif len(stemmed_query_list) == 1:
        #list to store the returned urls
        results = []
        #get position of word from index of index dictionary
        word_position = index_of_index[stemmed_query_list[0]]
        #jump to line in file with that word
        merged_index_file.seek(word_position)
        #load the posting list line as a list
        posting_list = json.loads(merged_index_file.readline().split(':')[1].replace('\n',''))
        #adds important word score for each document with that word
        for posting in posting_list:
            if posting[2]:
                posting[1] *= 3
        #sorts the posting list
        posting_list.sort(key = lambda x: x[1], reverse = True)
        #get total results found
        total_results_found = len(posting_list)
        #if there are 15 or more urls in postings list, put top 15 inside results
        if len(posting_list) >= 15:
            for tup in posting_list[:15]:
                results.append(docid_index[str(tup[0])])
        #if there are less than 5 urls in postings list, put them inside results
        else:
            for tup in posting_list:
                results.append(docid_index[str(tup[0])])
        #print the url results
        print('Results for ' + query_word_list[0] + ' are:')
        console_output.append('Results for ' + query_word_list[0] + ' are:')
        for url in results:
            print(url)
            console_output.append(url)
    
    # #scenario 2: find queries of length greater than 1
    else:
        #list that stores query terms and the length of its postings list
        rankings_list = []
        #put query terms and its postings list length into rankings list
        for word in stemmed_query_list:
            #get postion of word from index of index
            word_position = index_of_index[word]
            #jump to postion on inverted index file
            merged_index_file.seek(word_position)
            #put the query term and its posting list in rankings list as a tuple
            rankings_list.append((word, json.loads(merged_index_file.readline().split(':')[1])))
        #sort the rankings list by length of postings list in ascending order
        rankings_list.sort(key = lambda x: len(x[1]))
        #create a common url list that is initially the lowest length postings list
        #cut it to first 2000 if it is >= to length 2000, this to to improve query time
        common_url_list = rankings_list[0][1][:2000]
        #calculate tf*idf for the first term and times 3 if important
        for posting in common_url_list:
            tf = 1 + math.log10(posting[1])
            idf = math.log10(55393/len(rankings_list[0][1]))
            posting[1] = tf*idf
            if posting[2]:
                posting[1] *= 3
        #loop through all the other postings lists excluding the lowest length one
        for i in range(1, len(rankings_list)):
            #dictionary to store docids for a term mapped to tuple of freq & importance
            docid_dict = dict()
            #loop to get all docids for a term from its postings list
            for tup in rankings_list[i][1]:
                docid_dict[tup[0]] = (tup[1],tup[2])
            #check if all docids from the common url list is in the docid dictionary for all other terms
            for posting in common_url_list:
                #if docid is not in the docid dictionary for another term, remove the posting tuple
                if posting[0] not in docid_dict:
                    common_url_list.remove(posting)
                else:
                    #tfidf=(1+math.log10(term frequency for lopes in a document))*math.log10(55393/How many documents have lopes)
                    tf = 1 + math.log10(docid_dict[posting[0]][0])
                    idf = math.log10(55393/len(rankings_list[i][1]))
                    posting[1] += tf*idf
                    if docid_dict[posting[0]][1]:
                        posting[1] *= 3
        #sort the common urls by score
        common_url_list.sort(key = lambda x: x[1], reverse = True)
        #get total results found limited to 2000
        total_results_found = len(common_url_list)
        #list to store the returned urls
        results = []
        #if there are 15 or more urls, put top 15 inside results
        if len(common_url_list) >= 15:
            for tup in common_url_list[:15]:
                results.append(docid_index[str(tup[0])])
        #if there are less than 15 urls, put them inside results
        else:
            for tup in common_url_list:
                results.append(docid_index[str(tup[0])])
        #print the url results
        full_query = ' '.join(query_word_list)
        print('Results for ' + full_query + ' are:')
        console_output.append('Results for ' + full_query + ' are:')
        for url in results:
            print(url)
            console_output.append(url)
    merged_index_file.close()
    #end time and print it
    end_time = time.time()
    elapsed_time = (end_time - start_time)*1000
    print("Search completed in {:.4f} ms".format(elapsed_time))
    console_output.append("Search completed in {:.4f} ms".format(elapsed_time))
    print(str(total_results_found) + ' urls were found.')
    console_output.append(str(total_results_found) + ' urls were found.')

    #dict which hold informations and convert into JSON 
    response = {
        'query': query_word_string,
        'results': results,
        'elapsed_time': elapsed_time,
        'console_output': console_output
    }

    return jsonify(response)

#running web GUI
if __name__ == '__main__':
    app.run(port=5001)
