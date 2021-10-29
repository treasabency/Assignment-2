import re
import csv
import math
from collections import Counter

# Data Cleaning
def cleanDoc(d):
    text = d.lower()
    text = re.sub("\s+", ' ', text)
    text = re.sub(r'http\S+', '',text)
    text = re.sub(r'www\S+', '', text)
    text = re.sub('[\'",:!@#$%()]', '', text)
    text = re.sub(r'[^a-zA-Z0-9_]', ' ', text)
    return text

# Remove stopwords
def remStop(d):
    with open('stopwords.txt', 'r') as stopwords:
        stopwords = re.split('\n', stopwords.read())
        words = d.split()
        final = [word for word in words if word not in stopwords]
        result = ' '.join(final)
        return result

# Stemming and Lemmatization
def stem_lem(word):
    if re.search('[a-zA-Z0-9]*ly$', word):
        return (word[0:len(word)-2])

    if re.search('[a-zA-Z0-9]*ing$', word):
        return (word[0:len(word)-3])

    if re.search('[a-zA-Z0-9]*ment$', word):

        return (word[0:len(word)-4])
    return word

# Term Frequency 
def calculate_TF(word_frequency_list):
    total_word = 0
    final_dict = []
    for word, counter in word_frequency_list:
        total_word += counter

    for word, counter in word_frequency_list:
        tf = counter/total_word
        final_dict.append((word, tf))
    return final_dict

# Lists unique words from a file
def unique(d):
    infile = open(d, 'r')
    infile = infile.read()
    unique = []
    for word in infile.split():
        if word not in unique:
            unique.append(word)
    return unique

# Inverse Document Frequency
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
        # if word count is 0 or word count = doc_count, idf = 1
        if word_dict[key] == 0 or word_dict[key] == doc_count:   
            idf = 1
            idf_list.append((key, idf))
        else:
            idf = math.log(doc_count/word_dict[key]) + 1
            idf_list.append((key, idf))
    return idf_list

# TF-IDF Calculator
def calculate_TFIDF (tf, idf):
    tfidf_list = []
    for i in range(0, len(tf)):
        if tf[i][0] == idf[i][0]:
            tfidf = tf[i][1] * idf[i][1]
            tfidf_list.append((tf[i][0], round(tfidf, 2)))
    return tfidf_list

# Word count for words in a file
def term_freq (filename):
    with open(filename, 'r') as file:
        input_ = file.read()
        c = Counter(input_.split())
        freq = c.most_common()
    return freq

preproc_docs = []

with open('test.txt', 'r') as all_files:
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

# word count dictionary
TF_values = dict()
for file in preproc_docs:
    TF_values[file] = term_freq(file)

# term frequency dictionary
TF = dict()
for key, value in TF_values.items():
    TF[key] = calculate_TF(value)

# inverse document frequency dictionary
IDF = dict()
for key, value in TF_values.items():
    IDF[key] = calculate_IDF(value)

# top 5 TF-IDF for each document
TF_IDF = dict()
for key in TF:
    tf = sorted(TF[key], key=lambda tup: tup[0])
    idf = sorted(IDF[key], key=lambda tup: tup[0])
    TF_IDF[key] = calculate_TFIDF(tf, idf)
    top_5 = (sorted(TF_IDF[key], key=lambda tup: -tup[1]))[0:5]
    index = key.index("_")
    output = open('tfidf_' + key[index+1:], 'w')
    output.write(str(top_5))
    output.close()
