import re

def cleanDoc(d):
    text = d.lower()
    text = re.sub(r'http\S+', '',text)
    text = re.sub(r'www\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    text = re.sub("\s+", " ", text)
    #print(text.split())
    return text.split()

string = "Hello3 I am BINA. www.hylo        !@# everyone@hello.       JIHN)  https://world.com))"


def remStop(d):
    with open('stopwords.txt', 'r') as stopwords:
        stopwords = re.split('\n', stopwords.read())
        final = [word for word in d if word not in stopwords]
    #print(final)
    return final
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

print(stem_lem("punishment"))