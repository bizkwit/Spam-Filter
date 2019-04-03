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



def build_vocabulary(category, classification, filter_stop_words,filter_word_length):
    for document in category:
        path = "train\\"
        path += document
        # print(path)
        data = open(path, "r", encoding="Latin-1")
        for line in data:
            to_print = line.lower()
            to_print = re.split('[^a-zA-Z]+', to_print)
            for word in to_print:
                if filter_word_length or len(word)==0:
                    if len(word)==0 or len(word)<=2 or len(word)>=9:
                        continue
                if not filter_stop_words:
                    if word not in vocabulary:
                        vocabulary[word] = [0, 0]    # adding the new combination to vocabulary
                    vocabulary[word][classification.value] += 1
                    word_count[classification.value] += 1
                elif not verify_if_stop_word(word):
                    if word not in vocabulary:
                        vocabulary[word] = [0, 0]    # adding the new combination to vocabulary
                    vocabulary[word][classification.value] += 1
                    word_count[classification.value] += 1


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


def save_model(file_name, smoothing_value=0.0, do_print=False):
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
    with open(file_name, 'w') as file:
        file.write(model)
    if do_print:
        print(model)


def test_classify(file_name, category, classification, file_counter = 0, do_print=False, smoothing_value=0.5):
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
        data = open(path, "r", encoding="Latin-1")
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
    with open(file_name, 'a') as file:
        file. write(classified_emails)
    if do_print:
        print(classified_emails.rstrip())
    return file_counter


def task_selection():
    run_again = True
    while run_again:
        print("=================================================================")
        print("\t\t\t SPAM FILTER - MAIN MENU")
        print("=================================================================")
        print("Here are your option:\n\t 1. Task 1: Building the model \n\t 2. Task 2: Building and evaluating the classifier\n\t 3. Task 3: Experiment with your Classifier")
        user_input = input("Please choose your task (1-3): ")
        #//////////////TASK 1\\\\\\\\\\\\\\\
        if user_input is "1":
            HAM.clear()
            SPAM.clear()
            print("Running Task 1\n")
            print("Training....")
            process_files("train")
            process_stop_word("English-Stop-Words.txt")
            build_vocabulary(HAM, Classification.HAM, False, False)
            build_vocabulary(SPAM, Classification.SPAM, False, False)
            with open('model.txt', 'w') as file:
                file. write('')
            save_model('model.txt',0.5, False)
            print("Training DONE!\n")
            answer = input("would you like to run another task? (y/n): ")
            if answer == "n":
                print("GoodBye")
                run_again = False
        #//////////////TASK 2\\\\\\\\\\\\\\\
        elif user_input is "2":
            HAM.clear()
            SPAM.clear()
            print("Running Task 2\n")
            print("Testing....")
            process_files("train")
            process_stop_word("English-Stop-Words.txt")
            build_vocabulary(HAM, Classification.HAM, False, False)
            build_vocabulary(SPAM, Classification.SPAM, False, False)
            HAM.clear()
            SPAM.clear()
            process_files("test")
            file_counter = 0
            with open('baseline-result.txt', 'w') as file:
                file. write('')
            file_counter = test_classify('baseline-result.txt', HAM, Classification.HAM, file_counter, False)
            test_classify('baseline-result.txt', SPAM, Classification.SPAM, file_counter, False)
            print("Testing DONE!\n")
            answer = input("would you like to run another task? (y/n): ")
            if answer == "n":
                print("GoodBye")
                run_again = False
        #//////////////TASK 3\\\\\\\\\\\\\\\
        #~~~~~~~ NOT DONE ~~~~~~~
        elif user_input is "3":
            print("Running task 3: experiments \n")
            experiment_run = True
            while experiment_run:
                u_input = input("which experiment would you like to run? (2-5):")
                if u_input == "2":
                    HAM.clear()
                    SPAM.clear()
                    print("running Experiment 2 : Stop-word Filtering")
                    process_files("train")
                    process_stop_word("English-Stop-Words.txt")
                    build_vocabulary(HAM, Classification.HAM, True)
                    build_vocabulary(SPAM, Classification.SPAM, True)
                    save_model('stopword-model.txt',0.5,False)
                    HAM.clear()
                    SPAM.clear()
                    process_files("test")
                    file_counter = 0
                    file_counter = test_classify('stopword-result.txt', HAM, Classification.HAM, file_counter, False)
                    test_classify('stopword-result.txt', SPAM, Classification.SPAM, file_counter, False)
                    print("Experiment DONE!")
                    answer2 = input("run another experiemnt? (y/n): ")
                    if answer2 == "n":
                        experiment_run = False
                
                elif u_input == "3":
                    HAM.clear()
                    SPAM.clear()
                    print("running Experiment 3 : Word Length Filtering")
                    process_files("train")
                    process_stop_word("English-Stop-Words.txt")
                    build_vocabulary(HAM, Classification.HAM, True, True)
                    build_vocabulary(SPAM, Classification.SPAM, True, True)
                    save_model('wordlength-model.txt',0.5,False)
                    HAM.clear()
                    SPAM.clear()
                    process_files("test")
                    file_counter = 0
                    file_counter = test_classify('wordlength-result.txt', HAM, Classification.HAM, file_counter, False)
                    test_classify('wordlength-result.txt', SPAM, Classification.SPAM, file_counter, False)
                    print("Experiment DONE!")
                    answer2 = input("run another experiemnt? (y/n): ")
                    if answer2 == "n":
                        experiment_run = False
                
                elif u_input == "4":
                    HAM.clear()
                    SPAM.clear()
                    answer2 = input("run another experiemnt? (y/n): ")
                    if answer2 == "n":
                        experiment_run = False
               
                elif u_input == "5":
                    HAM.clear()
                    SPAM.clear()
                    answer2 = input("run another experiemnt? (y/n): ")
                    if answer2 == "n":
                        experiment_run = False
            
            
            answer = input("would you like to run another task? (y/n): ")
            if answer == "n":
                print("GoodBye")
                run_again = False

task_selection()
