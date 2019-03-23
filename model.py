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

get_list_of_words()
print(SPAM)
#a_uniq, counts = np.unique(SPAM, return_counts=True)
#voc = dict(zip(a_uniq, counts))
#print(voc)
