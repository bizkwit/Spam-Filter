import numpy as np
import math as math
from enum import Enum
import re as re
import sys as sys
import os
import matplotlib as mpl

SPAM = []
HAM = []
STOPWORDS = []

word_count = [0, 0]
vocabulary = dict()


class Classification(Enum):
    HAM = 0
    SPAM = 1


# ~~~~~~~ HELPER METHOD ~~~~~~~
def process_stop_word(file):
    words = open(file, "r")
    for word in words:
        STOPWORDS.append(word.replace("\n", ''))


def verify_if_stop_word(word):
    is_stop_word = False
    for stop_word in STOPWORDS:
        if stop_word == word:
            is_stop_word = True
            break
    return is_stop_word


# !!!!!!!!!!NOT DONE!!!!!!!!!!!!#
def build_2_gram_vocabulary(category, classification):
    for document in category:
        path = "train\\"
        path += document
        # print(path)
        data = open(path, "r")
        for line in data:
            to_print = line.lower()
            to_print = re.split('[^a-zA-Z]+', to_print)
            prev_word = None
            for word in to_print:
                if len(word) == 0:
                    continue
                if not verify_if_stop_word(word):
                    if prev_word is None:
                        prev_word = word
                    if word in vocabulary:
                        if prev_word not in vocabulary[word]:
                            vocabulary[word][prev_word] = [0, 0]
                    else:
                        vocabulary[word] = {word: [0, 0]}   # adding the new word to the vocabulary
                        vocabulary[word][prev_word] = [0, 0]    # adding the new combination to vocabulary
                    vocabulary[word][prev_word][classification.value] += 1
                    word_count[classification.value] += 1
            # print(to_print)


def build_vocabulary(category, classification, filterStopWords):
    for document in category:
        path = "train\\"
        path += document
        # print(path)
        data = open(path, "r", encoding="ISO-8859-1")
        for line in data:
            to_print = line.lower()
            to_print = re.split('[^a-zA-Z]+', to_print)
            for word in to_print:
                if len(word) == 0:
                    continue
                if not filterStopWords:
                    if word not in vocabulary:
                        vocabulary[word] = [0, 0]    # adding the new combination to vocabulary
                    vocabulary[word][classification.value] += 1
                    word_count[classification.value] += 1
                elif not verify_if_stop_word(word):
                    if word not in vocabulary:
                        vocabulary[word] = [0, 0]    # adding the new combination to vocabulary
                    vocabulary[word][classification.value] += 1
                    word_count[classification.value] += 1
            # print(to_print)


def process_files(folder):
    """
    process file of a folder and uses helper method to categorize each file to its designated place
    attributes:
    - folder: a folder from where files should be read and processed
    """
    # store all the files from the foler in a list for further processing
    files = []
    for i in os.listdir(folder):
        files.append(i)
    # process each file from the list of files and store into its designated place
    for document in files:
        categorize(document)


def categorize(file):
    """
    categorizes given file whether it is ham file or spam file using regex
    attributes:
    - file: given file to process
    """
    spam_filter = re.compile("spam", )  # re.compile("spam")
    if spam_filter.search(file) is None:
        HAM.append(file)
    else:
        SPAM.append(file)


def save_model(smoothing_value=0.0, do_print=False):
    i = 0
    total_vocabulary_words = len(vocabulary)
    total_vocabulary_words += total_vocabulary_words * smoothing_value
    ham_word_count = word_count[Classification.HAM.value] + total_vocabulary_words
    spam_word_count = word_count[Classification.SPAM.value] + total_vocabulary_words
    model = ""
    for word, frequencies in sorted(vocabulary.items()):
        i += 1
        ham_word_frequency = vocabulary[word][Classification.HAM.value] + smoothing_value
        spam_word_frequency = vocabulary[word][Classification.SPAM.value] + smoothing_value
        model += ("%d  %s  %g  %g  %g  %g\n" % (i, word, ham_word_frequency, ham_word_frequency/ham_word_count,
                                                spam_word_frequency, spam_word_frequency/spam_word_count))
    with open('model.txt', 'w') as file:
        file.write(model)
    if do_print:
        print(model)


def test_classify(category, classification, file_counter = 0, do_print=False, smoothing_value=0.5):
    num_spam_emails = len(SPAM)
    num_hum_emails = len(HAM)
    total_vocabulary_words = len(vocabulary)
    total_vocabulary_words += total_vocabulary_words * smoothing_value
    ham_word_count = word_count[Classification.HAM.value] + total_vocabulary_words
    spam_word_count = word_count[Classification.SPAM.value] + total_vocabulary_words
    classified_emails = ""
    for document in category:
        file_counter += 1
        path = "test\\"
        path += document
        ham_probability = math.log10(num_hum_emails/(num_spam_emails + num_hum_emails))
        spam_probability = math.log10(num_spam_emails/(num_spam_emails + num_hum_emails))
        data = open(path, "r", encoding="Latin1")
        for line in data:
            line = line.lower()
            line = re.split('[^a-zA-Z]+', line)
            for word in line:
                if len(word) == 0:
                    continue
                if not verify_if_stop_word(word) and word in vocabulary:
                    ham_word_probability = (vocabulary[word][Classification.HAM.value] + smoothing_value)/ham_word_count
                    spam_word_probability = (vocabulary[word][Classification.SPAM.value] + smoothing_value)/spam_word_count
                    ham_probability += math.log10(ham_word_probability)
                    spam_probability += math.log10(spam_word_probability)
        if ham_probability > spam_probability:
            file_classification = Classification.HAM
        else:
            file_classification = Classification.SPAM
        if file_classification != classification:
            right_wrong = "wrong"
        else:
            right_wrong = "right"
        classified_email = ("%d  %s  %s  %g  %g  %s  %s\n" % (file_counter, document, file_classification.name.lower(),
                                                              ham_probability, spam_probability,
                                                              classification.name.lower(), right_wrong))
        classified_emails += classified_email
    with open('baseline-result.txt', 'a') as file:
        file. write(classified_emails)
    if do_print:
        print(classified_emails.rstrip())
    return file_counter


print("Training....")
process_files("train")
process_stop_word("English-Stop-Words.txt")
build_vocabulary(HAM, Classification.HAM, False)
build_vocabulary(SPAM, Classification.SPAM, False)
save_model(0.5, False)
print("Training DONE!")

print("Testing....")
HAM = []
SPAM = []
process_files("test")
file_counter = 0
file_counter = test_classify(HAM, Classification.HAM, file_counter, True)
test_classify(SPAM, Classification.SPAM, file_counter, True)
