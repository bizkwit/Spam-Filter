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
                cleanList = remove_values_from_list(toPrint, '')
                SPAM.extend(cleanList)
        if "ham" in i:
            data = open(path+i, "r", encoding="ISO-8859-1")
            for line in data:
                toPrint = line.lower()
                toPrint = re.split('[^a-zA-Z]+', toPrint)
                cleanList = remove_values_from_list(toPrint, '')
                HAM.extend(cleanList)
    SPAM.sort()
    HAM.sort()

def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]

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
# filtered_ham, filtered_spam = filter_data()
# filtered_spam.sort(reverse=True)
print(SPAM)
#a_uniq, counts = np.unique(SPAM, return_counts=True)
#voc = dict(zip(a_uniq, counts))
#print(voc)
