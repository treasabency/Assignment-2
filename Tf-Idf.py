import re
import csv
import math
from collections import Counter
import os
def cleanDoc(d):
    text = d.lower()
    text = re.sub("\s+", ' ', text)
    text = re.sub(r'http\S+', '',text)
    text = re.sub(r'www\S+', '', text)
    text = re.sub('[\'",:!@#$%()]', '', text)
    text = re.sub(r'[^a-zA-Z0-9_]', ' ', text)
    return text


def remStop(d):
    with open('stopwords.txt', 'r') as stopwords:
        stopwords = re.split('\n', stopwords.read())
        words = d.split()
        final = [word for word in words if word not in stopwords]
        result = ' '.join(final)
        return result


#This function takes in a word, and returns a root version of the word
def stem_lem(word):
    if re.search('[a-zA-Z0-9]*ly$', word):
        return (word[0:len(word)-2])
        #return word without ly, but check if theres a extra l at the end
    if re.search('[a-zA-Z0-9]*ing$', word):
        return (word[0:len(word)-3])
        #need to take in consideration of words like dying, lying
    if re.search('[a-zA-Z0-9]*ment$', word):
        #need to consider words like moment, cement
        return (word[0:len(word)-4])
    return word
#print(remStop(cleanDoc(string)))

#input dict: [[word1, counter], [word2, counter], etc...]
def calculate_TF(word_frequency_list):
    #calculate total amount of words
    total_word = 0
    final_dict = {}
    for word, counter in word_frequency_list:
        total_word += counter
    #calculate the TF of each word
    for word, counter in word_frequency_list:
        tf = counter/total_word
        final_dict[word] = tf
    return final_dict
#returns {word: tf, word1: tf} of each doc

def unique(d):
    infile = open(d, 'r')
    infile = infile.read()
    unique = []
    for word in infile.split():
        if word not in unique:
            unique.append(word)
    return unique

def calculate_IDF(doc):
    word_dict = {}      # format: {word1:count, word2, count,...}
    idf_list = []       # fromat: [(word1, count), (word2,count),...]
    doc_count = len(preproc_docs)
    words = [a[0] for a in doc]
    for file in preproc_docs:
        temp = unique(file)
        for word in words:
            if word in temp:
                if word in word_dict.keys():
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
    for key in word_dict:
        if word_dict[key] == 3 or word_dict[key] == 0:      # if word count is 0 or 3 (since log(3/3) = 0)
            idf = 1
            idf_list.append((key, idf))
        else:
            idf = math.log(doc_count/word_dict[key])
            idf_list.append((key, idf))
    return idf_list


#takes in a document
def term_freq (filename):
    with open(filename, 'r') as file:
        input_ = file.read()
       # print(f'{filename}: {input_}')
        c = Counter(input_.split())
       # print(c)
        freq = c.most_common()
    #print(freq)
    return freq
#returns [(word, counter), (word2, counter), etc]

preproc_docs = []
with open('tfidf_docs.txt', 'r') as all_files:
    reader = csv.reader(all_files)
    for row in reader:
        result = []
        file_name = ''.join(row)
        with open(file_name) as inpfile:
            input1 = inpfile.read()
            clean = cleanDoc(input1)
            cleaner = remStop(clean)
            words = cleaner.split()
            for word in words:
                result.append(stem_lem(word))
            final = ' '.join(result)
            preproc_docs.append('preproc_'+ file_name.split('.')[0])
            output = open('preproc_'+ file_name.split('.')[0], 'w')
            output.write(final)
            output.close()

TF_values = dict()
for file in preproc_docs:
    TF_values[file] = term_freq(file)
    
TF = dict()
for key, value in TF_values.items():
    TF[key] = calculate_TF(value)

IDF = dict()
for key, value in TF_values.items():
    IDF[key] = calculate_IDF(value)

#print(TF)
print(IDF)
