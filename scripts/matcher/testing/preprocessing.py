from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import nltk
import string
import os

from wordcloud import WordCloud
import matplotlib.pyplot as plt

lemmatizer = WordNetLemmatizer()
stemmer = LancasterStemmer()

def _flatten(list):
  for i in list:
    for j in i:
      yield j

def remove_newline(text):
    return text.replace("\n", " ")

def to_lower(text):
    return text.lower()

def remove_source_tags(text):
    groups = ['']
    for i in text:
        if i == '[':
            groups.append(i)
        elif i == ']' and len(groups) > 1 and groups[-1][1:].isdigit():
            groups.pop()
        else:
            groups[-1] += i
        #print(groups)
    return "".join(groups)

def remove_punctuation(text):
    for pt in string.punctuation:
        text = text.replace(pt,"")
    return text

def _stem(token):
    return stemmer.stem(token)

def _lemmatize(token):
    return lemmatizer.lemmatize(token)

def tokenize_and_normalize(text):
    data = [] #list of lists of tokenized words
    # iterate through each sentence in the file
    for sent in sent_tokenize(text):
        temp = []
        # tokenize the sentence into words
        for token in word_tokenize(sent):
            token = str(_stem(token))
            token = str(_lemmatize(token))
            temp.append(token)
        data.append(temp)
    return data

def remove_stop_words(tokenized_sents):
    data = tokenized_sents
    stop_words = nltk.corpus.stopwords.words('english')
    while len(stop_words):
        for s, sent in enumerate(data):
            delete_list = []

            for t, token in enumerate(sent):
                if token in stop_words:
                    delete_list.append(t)
            for i, t in enumerate(delete_list):
                del data[s][t-i]
        stop_words = []

        tokens = _flatten(data)
        frequ_dist = nltk.FreqDist(tokens)

        frequ_list = sorted(frequ_dist,key=frequ_dist.__getitem__, reverse=True)[0:50]

        print("50 most frequent words: \n", frequ_dist)
        des = input("Delete 50 words? (number/yes/no): ")
        if des == "yes":
            stop_words = frequ_list[:50]
        elif des.isdigit():
            stop_words = frequ_list[:int(des)]
        else:
            break

    # wordcloud = WordCloud().generate_from_frequencies(frequ_dist)
    # plt.imshow(wordcloud)
    # plt.axis("off")
    # plt.show()



    return data


def prep_run(text):
    text = to_lower(text)
    text = remove_source_tags(text)
    text = remove_punctuation(text)
    data = tokenize_and_normalize(text)
    data = remove_stop_words(data)
    return data

if __name__ == "__main__":
    s = ""
    for file_name in os.listdir("data"):
        with open("data/"+file_name, "r", encoding="mac_roman") as sample:
            print(file_name)
            try:
                s += sample.read() + " "
            except Exception as e:
                print("Err", file_name, e)

    print("Vocab:", set(_flatten(prep_run(s))))
