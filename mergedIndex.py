import json 
import fileinput

#creates the mergedIndex.txt file and writes contents from the first partial index
def createMergedIndexFile():
    with open('mergedIndex.txt', 'w') as create_file:
        #loads the first partial index to a dictionary
        with open('m1invertedindex5000.json', 'r') as file:
            part_inverted_index = json.load(file)
        #loops through each token and posting, sorts the posting by importance and term frequency, 
        #and writes it to the file
        for tok,post in part_inverted_index.items():
            post.sort(key = lambda x : (-x[2],-x[1]))
            create_file.write(tok + ':' + str(post) + '\n')

#modifies the mergedIndex.txt file for all the partial indexes
def mergeAllIndexes(filename):
    #creates a index of index for the current mergedIndex.txt file
    with open('mergedIndex.txt', 'r') as read_file:
        word_pos = dict()
        position = 0
        for line in read_file:
            word_pos[line.split(':')[0]] = position
            position += len(line)
    #loads the partial index as a dictionary
    with open(filename, 'r') as file:
        part_inverted_index = json.load(file)
    print("Merging " + filename)
    with open('mergedIndex.txt', 'a+') as merged_index_file:
        dele_pos = set()
        #loops through the partial index
        for tok,post in part_inverted_index.items():
            #if a word is in the file already, add position of line to dele_pos set,
            #load the line, append the list, sort the list, write it to the end of the file
            if tok in word_pos:
                merged_index_file.seek(word_pos[tok])
                dele_pos.add(word_pos[tok])
                to_append_list = json.loads(merged_index_file.readline().split(':')[1].replace('\n',''))
                to_append_list += post
                to_append_list.sort(key = lambda x : (-x[2],-x[1]))
                merged_index_file.seek(0,2)
                merged_index_file.write(tok + ':' + str(to_append_list) + '\n')
            #if a word is not in the file, write it to the end of the file
            else:
                post.sort(key = lambda x : (-x[2],-x[1]))
                merged_index_file.seek(0,2)
                merged_index_file.write(tok + ':' + str(post) + '\n')
    #loop through all the lines in mergedIndex.txt while also calculating position,
    #if one of the lines are in dele_pos, delete that line because it is a duplicate
    #of the word in the file not yet appended
    pos = 0
    for line in fileinput.input('mergedIndex.txt', inplace=True):
        if pos in dele_pos:
            pos += len(line)
            line = ''
            print(line, end='')
        else:
            pos += len(line)
            print(line, end='')

#merges all the partial docID index files
def mergeDocId(files_list):
    #dict to store all the docId's merged with it's url
    merged_docid_index = dict()
    #loop through all the files for indexes and puts docid and url to merged_docid_index
    for file in files_list:
        with open(file, 'r') as file:
            part_docid_index = json.load(file)
            for id, url in part_docid_index.items():
                if id not in merged_docid_index:
                    merged_docid_index[id] = url  
    #dump the merged docid index into a json file
    with open('merged_docid_index.json', 'w') as merged_docid_index_file:
        json.dump(merged_docid_index, merged_docid_index_file)

#indexes the index
def indexOfIndex():
    #dictionary to store all words and its position on the mergedIndex.txt file
    indexed_index = dict()
    with open('mergedIndex.txt', 'r') as merged_index_file:
        #current position of file
        position = 0
        #loop through every line of the mergedIndex file
        for line in merged_index_file:
            #adds word and its file position to the index of index dictionary
            indexed_index[line.split(':')[0]] = position
            #adds position by the length of the line
            position += len(line)
    #dump the dictionary into a json file
    with open('indexofindex.json', 'w') as indexofindex_file:
        json.dump(indexed_index, indexofindex_file)

if __name__ == '__main__':
    #list of every partial index file excluding the first
    part_files_list = ['m1invertedindex10000.json', 'm1invertedindex15000.json',
                  'm1invertedindex20000.json', 'm1invertedindex25000.json', 'm1invertedindex30000.json',
                    'm1invertedindex35000.json', 'm1invertedindex40000.json', 'm1invertedindex45000.json',
                        'm1invertedindex50000.json', 'm1invertedindex55000.json', 'm1invertedindexEnd.json']
    #list of every docid index file
    doc_id_list = ['m1docindex5000.json', 'm1docindex10000.json', 'm1docindex15000.json', 'm1docindex20000.json',
                    'm1docindex25000.json', 'm1docindex30000.json', 'm1docindex35000.json', 'm1docindex40000.json',
                        'm1docindex45000.json', 'm1docindex50000.json', 'm1docindex55000.json', 'm1docindex.json']
    #runs all methods to merge index, docidindex, and index of index
    mergeDocId(doc_id_list)
    createMergedIndexFile()
    for filename in part_files_list:
        mergeAllIndexes(filename)
    indexOfIndex()
