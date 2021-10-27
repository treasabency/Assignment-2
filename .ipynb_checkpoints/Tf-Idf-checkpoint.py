import re
import csv
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

#continue working on this
with open('tfidf_docs.txt', 'r') as all_files:
    reader = csv.reader(all_files)
    for _, row in enumerate(reader):
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
            output = open('preproc_'+ file_name.split('.')[0], 'w')
            output.write(final)

#input dict: {[counter, word1], [counter, word2], etc...}

def calculate_TF(word_frequency_list):
    #calculate total amount of words
    total_word = 0
    final_dict = {}
    for counter, word in word_frequency_list:
        total_word += counter
    #calculate the TF of each word
    for counter, word in word_frequency_list:
        tf = counter/total_word
        final_dict[word] = tf
    
    #for key, value in final_dict.items():
        #print(key, "   ", value)
    return final_dict

#take in a dict of {doc1: [[word, tf], [word2, tf]], doc2: [[word, tf], [word2, tf]], etc}
def calculate_IDF(doc_dicts):
    #find the total number of docs with len(dict)
    #start going through all the docs word list one by one,
        #check how many docs the words are in by comparing if word in docs
    #compute the IDF for that word by log(total_doc/docs_appeared_in)
    #repeat for every word
    
    #it should return {word: IDF, word2: IDF, word3: IDF, etc}
    return
calculate_TF([(3, "the"), (2, "bye"), (1, "hand"), (6, "hi")])