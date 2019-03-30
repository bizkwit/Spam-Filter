import numpy as np
import math as math
import re as re
import sys as sys
import os
import matplotlib as mpl
from os import listdir
from os.path import isfile, join

SPAM=[]
HAM=[]
filtered_ham = []
filtered_spam = []

def get_list_of_words():
    path = "train/"
    for i in os.listdir("train"):
        if "spam" in i:
            data = open(path+i, "r", encoding="ISO-8859-1")
            for line in data:
                toPrint = line.lower()
                toPrint = re.split('[^a-zA-Z]+', toPrint)
                toPrint.remove('')
                SPAM.extend(toPrint)
        if "ham" in i:
            data = open(path+i, "r", encoding="ISO-8859-1")
            for line in data:
                toPrint = line.lower()
                toPrint = re.split('[^a-zA-Z]+', toPrint)
                toPrint.remove('')
                HAM.extend(toPrint)
    SPAM.sort(reverse=True)
    HAM.sort(reverse=True)

def filter_data():
    stopwords = []
    stopwords.extend('')
    with open("English-Stop-Words.txt", "r") as file:
        words = [line.rstrip('\n') for line in file.readlines()]
        for word in words:
            stopwords.append(word)
    stop_set = set(stopwords)
    ham_set = set(HAM)
    spam_set = set(SPAM)
    return_ham = ham_set-stop_set
    return_spam = spam_set-stop_set
    return list(return_ham), list(return_spam)


get_list_of_words()
filtered_ham, filtered_spam = filter_data()
filtered_spam.sort(reverse=True)
print(SPAM)
#a_uniq, counts = np.unique(SPAM, return_counts=True)
#voc = dict(zip(a_uniq, counts))
#print(voc)
