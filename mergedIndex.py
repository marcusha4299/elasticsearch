import json 
import fileinput

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

    for post in merged_inverted_index.values():
        post.sort(key = lambda x : (-x[2],-x[1]))

    # with open('merged_invertedindex.json', 'w') as merged_index_file:
    #     json.dump(dict(sorted(merged_inverted_index.items())), merged_index_file)
    with open('merged_inverted_index.txt', 'w') as merged_index_file:
        for tok,post in dict(sorted(merged_inverted_index.items())).items():
            merged_index_file.write(tok + ':' + str(post) + '\n')

def createMergedIndexFile():
    with open('mergedIndex.txt', 'w') as create_file:
        with open('m1invertedindex5000.json', 'r') as file:
            part_inverted_index = json.load(file)
        for tok,post in part_inverted_index.items():
            post.sort(key = lambda x : (-x[2],-x[1]))
            create_file.write(tok + ':' + str(post) + '\n')

def mergeAllIndexes(filename):
    with open('mergedIndex.txt', 'r') as read_file:
        word_pos = dict()
        position = 0
        for line in read_file:
            word_pos[line.split(':')[0]] = position
            position += len(line)
    with open(filename, 'r') as file:
        part_inverted_index = json.load(file)
    print("Merging " + filename)
    with open('mergedIndex.txt', 'a+') as merged_index_file:
        dele_pos = set()
        for tok,post in part_inverted_index.items():
            if tok in word_pos:
                merged_index_file.seek(word_pos[tok])
                dele_pos.add(word_pos[tok])
                to_append_list = json.loads(merged_index_file.readline().split(':')[1].replace('\n',''))
                to_append_list += post
                to_append_list.sort(key = lambda x : (-x[2],-x[1]))
                merged_index_file.seek(0,2)
                merged_index_file.write(tok + ':' + str(to_append_list) + '\n')
            else:
                post.sort(key = lambda x : (-x[2],-x[1]))
                merged_index_file.seek(0,2)
                merged_index_file.write(tok + ':' + str(post) + '\n')
    pos = 0
    for line in fileinput.input('mergedIndex.txt', inplace=True):
        if pos in dele_pos:
            pos += len(line)
            line = ''
            print(line, end='')
        else:
            pos += len(line)
            print(line, end='')

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

def indexOfIndex():
    indexed_index = dict()
    with open('mergedIndex.txt', 'r') as merged_index_file:
        position = 0
        for line in merged_index_file:
            indexed_index[line.split(':')[0]] = position
            position += len(line)

    with open('indexofindex.json', 'w') as indexofindex_file:
        json.dump(indexed_index, indexofindex_file)

if __name__ == '__main__':
    files_list = ['m1invertedindex5000.json', 'm1invertedindex10000.json', 'm1invertedindex15000.json',
                  'm1invertedindex20000.json', 'm1invertedindex25000.json', 'm1invertedindex30000.json',
                    'm1invertedindex35000.json', 'm1invertedindex40000.json', 'm1invertedindex45000.json',
                        'm1invertedindex50000.json', 'm1invertedindex55000.json', 'm1invertedindexEnd.json']
    part_files_list = ['m1invertedindex10000.json', 'm1invertedindex15000.json',
                  'm1invertedindex20000.json', 'm1invertedindex25000.json', 'm1invertedindex30000.json',
                    'm1invertedindex35000.json', 'm1invertedindex40000.json', 'm1invertedindex45000.json',
                        'm1invertedindex50000.json', 'm1invertedindex55000.json', 'm1invertedindexEnd.json']
    doc_id_list = ['m1docindex5000.json', 'm1docindex10000.json', 'm1docindex15000.json', 'm1docindex20000.json',
                    'm1docindex25000.json', 'm1docindex30000.json', 'm1docindex35000.json', 'm1docindex40000.json',
                        'm1docindex45000.json', 'm1docindex50000.json', 'm1docindex55000.json', 'm1docindex.json']
    # mergeInvertedIndex(files_list)
    mergeDocId(doc_id_list)
    createMergedIndexFile()
    for filename in part_files_list:
        mergeAllIndexes(filename)
    indexOfIndex()
