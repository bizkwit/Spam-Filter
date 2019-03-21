import numpy as np
import math as math
import re as re
import sys as sys
import os
import matplotlib as mpl

SPAM=[]
HAM=[]
#!!!!!!!!!!NOT DONE!!!!!!!!!!!!#
def build_vocabulary(category):
    for document in category:
        path = "train\\"
        path += document
        print(path)
        data = open(path,"r")
        for line in data:
            toPrint = line.lower()
            toPrint = re.split('[^a-zA-Z]+', toPrint)
            print(toPrint)
            

def process_files(folder):
    """
    process file of a folder and uses helper method to categorize each file to its designated place
    attributes:
    - folder: a folder from where files should be read and processed
    """
    #store all the files from the foler in a list for further processing
    files = []
    for i in os.listdir(folder):
            files.append(i)
    #process each file from the list of files and store into its designated place
    for document in files:
        categorize(document)

def categorize(file):
    """
    categorizes given file whether it is ham file or spam file using regex
    attributes:
    - file: given file to process
    """
    spam_filter = re.compile("spam",)   #re.compile("spam")
    if spam_filter.search(file) is None:
        HAM.append(file)
    else:
        SPAM.append(file)



process_files("train")
build_vocabulary(SPAM)
   
    
