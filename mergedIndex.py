import json 

def mergeInvertedIndex(files_list):
    #dictionary to store all the tokens
    merged_inverted_index = dict()
    #loop through all the files for indexes
    for file in files_list:
        with open(file, 'r') as file:
            part_inverted_index = json.load(file)
            for token, posting in part_inverted_index.items():
                if token not in merged_inverted_index:
                    merged_inverted_index[token] = posting
                else:
                    merged_inverted_index[token] += posting

    
    with open('merged_invertedindex.json', 'w') as merged_index_file:
        json.dump(merged_inverted_index, merged_index_file)
    # with open('merged_inverted_index.txt', 'w') as merged_index_file:
    #     for tok,post in merged_inverted_index.items():
    #         merged_index_file.write(tok + ':' + str(post) + '\n')

def mergeDocId(files_list):
    merged_docid_index = dict()
    #loop through all the files for indexes
    for file in files_list:
        with open(file, 'r') as file:
            part_docid_index = json.load(file)
            for id, url in part_docid_index.items():
                if id not in merged_docid_index:
                    merged_docid_index[id] = url

    
    with open('merged_docid_index.json', 'w') as merged_docid_index_file:
        json.dump(merged_docid_index, merged_docid_index_file)



if __name__ == '__main__':
    files_list = ['m1invertedindex5000.json', 'm1invertedindex10000.json', 'm1invertedindex15000.json',
                  'm1invertedindex20000.json', 'm1invertedindex25000.json', 'm1invertedindex30000.json',
                    'm1invertedindex35000.json', 'm1invertedindex40000.json', 'm1invertedindex45000.json',
                        'm1invertedindex50000.json', 'm1invertedindex55000.json', 'm1invertedindexEnd.json']
    doc_id_list = ['m1docindex5000.json', 'm1docindex10000.json', 'm1docindex15000.json', 'm1docindex20000.json',
                    'm1docindex25000.json', 'm1docindex30000.json', 'm1docindex35000.json', 'm1docindex40000.json',
                        'm1docindex45000.json', 'm1docindex50000.json', 'm1docindex55000.json', 'm1docindex.json']
    mergeInvertedIndex(files_list)
    mergeDocId(doc_id_list)