import json
import time
from nltk.stem import PorterStemmer
import math

if __name__ == '__main__':
    with open('merged_invertedindex.json', 'r') as merged_index_file:
        inverted_index = json.load(merged_index_file)

    with open('merged_docid_index.json', 'r') as merged_docid_file:
        docid_index = json.load(merged_docid_file)
    
    query_word_list = input("What is your query?: \n").lower().split()
    stemmed_query_list = []

    ps = PorterStemmer()

    for word in query_word_list:
        stemmed_query_list.append(ps.stem(word))
    
    start_time = time.time()

    #check if the query has stop words and remove them for M3
    
    #scenario 1: find queries of length 1
    if len(query_word_list) == 1:
        #check if query is not in the inverted index
        if stemmed_query_list[0] not in inverted_index:
            print('No search results for: ' + query_word_list[0])
        #if query is in the inverted index
        else:
            #list to store the returned urls
            results = []
            #sort the postings list for the query term by frequency
            sorted_ranking = inverted_index[stemmed_query_list[0]]
            sorted_ranking.sort(key = lambda x: x[1], reverse = True)
            #if there are 5 or more urls in postings list, put top 5 inside results
            if len(sorted_ranking) >= 5:
                for tup in sorted_ranking[:5]:
                    results.append(docid_index[str(tup[0])])
            #if there are less than 5 urls in postings list, put them inside results
            else:
                for tup in sorted_ranking:
                    results.append(docid_index[str(tup[0])])
            #print the url results
            print('Results for ' + query_word_list[0] + ' are:')
            for url in results:
                print(url)
    
    #scenario 2: find queries of length greater than 1
    #finished but may not be fully correct
    else:
        #list that stores query terms and the length of its postings list
        rankings_list = []
        #put query terms and its postings list length into rankings list
        for word in stemmed_query_list:
            rankings_list.append((word, len(inverted_index[word])))
        #sort the rankings list by length of postings list in ascending order
        rankings_list.sort(key = lambda x: x[1])
        #create a common url list that is initially the lowest length postings list
        common_url_list = inverted_index[rankings_list[0][0]]
        #calculate tf*idf for the first term and times 3 if important
        for posting in common_url_list:
            tf = 1 + math.log10(posting[1])
            idf = math.log10(55393/len(common_url_list))
            posting[1] = tf*idf
            if posting[2]:
                posting[1] *= 3
        #loop through all the other postings lists excluding the lowest length one
        for i in range(1, len(rankings_list)):
            #dictionary to store docids for a term mapped to tuple of freq & importance
            docid_dict = dict()
            #loop to get all docids for a term from its postings list
            for tup in inverted_index[rankings_list[i][0]]:
                docid_dict[tup[0]] = (tup[1],tup[2])
            #check if all docids from the common url list is in the docid dictionary for all other terms
            for posting in common_url_list:
                #if docid is not in the docid dictionary for another term, remove the posting tuple
                if posting[0] not in docid_dict:
                    common_url_list.remove(posting)
                else:
                    #tfidf=(1+math.log10(term frequency for lopes in a document))*math.log10(55393/How many documents have lopes)
                    tf = 1 + math.log10(docid_dict[posting[0]][0])
                    idf = math.log10(55393/len(inverted_index[rankings_list[i][0]]))
                    posting[1] += tf*idf
                    if docid_dict[posting[0]][1]:
                        posting[1] *= 3
        #sort the common urls by term frequency, but only for the term with lowest length postings list
        common_url_list.sort(key = lambda x: x[1], reverse = True)
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
        for url in results:
            print(url)
        
    end_time = time.time()
    elapsed_time = (end_time - start_time)*1000
    print("Search completed in {:.4f} ms".format(elapsed_time))
        
