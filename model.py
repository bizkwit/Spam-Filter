import math as math
from enum import Enum
import re as re
import os


class Metrics:

    def __init__(self):
        self.total_target = [0, 0]
        self.labeled = [0, 0]
        self.correctly = [0, 0]

    def get_accuracy(self, classification=None):
        accuracy = -1
        if classification is None:
            if not (self.total_target[0] == 0 and self.total_target[1] == 0):
                accuracy = (self.correctly[0] + self.correctly[1]) * 100/(self.total_target[0] + self.total_target[1])
        elif self.labeled[classification.value] != 0:
            accuracy = self.correctly[classification.value] * 100/self.total_target[classification.value]
        return accuracy

    def get_precision(self, classification=None):
        precision = -1
        if classification is None:
            if not (self.labeled[0] == 0 and self.labeled[1] == 0):
                precision = (self.correctly[0] + self.correctly[1]) * 100/(self.labeled[0] + self.labeled[1])
        elif self.labeled[classification.value] != 0:
            precision = self.correctly[classification.value] * 100/self.labeled[classification.value]
        return precision

    def get_recall(self, classification=None):
        recall = -1
        if classification is None:
            if not (self.total_target[0] == 0 and self.total_target[1] == 0):
                recall = (self.correctly[0] + self.correctly[1]) * 100/(self.total_target[0] + self.total_target[1])
        elif self.total_target[classification.value] != 0:
            recall = self.correctly[classification.value] * 100/self.total_target[classification.value]
        return recall

    def get_f1(self, classification=None):
        f1 = -1
        precision = self.get_precision(classification)
        recall = self.get_recall(classification)
        if not (precision <= 0 and recall <= 0):
            f1 = 2 * precision * recall/(precision + recall)
        return f1

    def print_metrics(self):
        print("\n\t\t\tSPAM\tHAM\t\tTOTAL")
        spam = self.get_accuracy(Classification.SPAM)
        ham = self.get_accuracy(Classification.HAM)
        total = self.get_accuracy()
        print("Accuracy:\t%0.2f%%\t%0.2f%%\t%0.2f%%" % (spam, ham, total))
        spam = self.get_precision(Classification.SPAM)
        ham = self.get_precision(Classification.HAM)
        total = self.get_precision()
        print("Precision:\t%0.2f%%\t%0.2f%%\t%0.2f%%" % (spam, ham, total))
        spam = self.get_recall(Classification.SPAM)
        ham = self.get_recall(Classification.HAM)
        total = self.get_recall()
        print("Recall:\t\t%0.2f%%\t%0.2f%%\t%0.2f%%" % (spam, ham, total))
        spam = self.get_f1(Classification.SPAM)
        ham = self.get_f1(Classification.HAM)
        total = self.get_f1()
        print("F1-measure:\t%0.2f%%\t%0.2f%%\t%0.2f%%\n" % (spam, ham, total))


class Classification(Enum):
    HAM = 0
    SPAM = 1


class Model:

    def __init__(self):
        # self.SPAM = []
        # self.HAM = []
        self.file_names = [[], []]
        self.STOPWORDS = []

        self.word_count = [0, 0]
        self.vocabulary = dict()
        self.metrics = Metrics()

    # ~~~~~~~ HELPER METHOD ~~~~~~~
    def process_stop_word(self, file):
        words = open(file, "r")
        for word in words:
            self.STOPWORDS.append(word.replace("\n", ''))

    def verify_if_stop_word(self, word):
        is_stop_word = False
        for stop_word in self.STOPWORDS:
            if stop_word == word:
                is_stop_word = True
                break
        return is_stop_word

    def build_vocabulary(self, filter_stop_words, filter_word_length):
        for i in range(2):
            category = self.file_names[i]
            for document in category:
                path = "train/"
                path += document
                # print(path)
                data = open(path, "r", encoding="Latin-1")
                for line in data:
                    to_print = line.lower()
                    to_print = re.split('[^a-zA-Z]+', to_print)
                    for word in to_print:
                        if filter_word_length or len(word) == 0:
                            if len(word) == 0 or len(word) <= 2 or len(word) >= 9:
                                continue
                        is_stop_word = False
                        if filter_stop_words:
                            is_stop_word = self.verify_if_stop_word(word)
                        if not is_stop_word:
                            if word not in self.vocabulary:
                                self.vocabulary[word] = [0, 0]  # adding the new combination to vocabulary
                            self.vocabulary[word][i] += 1
                            self.word_count[i] += 1

    def process_files(self, folder):
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
            self.categorize(document)

    def categorize(self, file):
        """
        categorizes given file whether it is ham file or spam file using regex
        attributes:
        - file: given file to process
        """
        spam_filter = re.compile("spam", )  # re.compile("spam")
        if spam_filter.search(file) is None:
            self.file_names[Classification.HAM.value].append(file)
        else:
            self.file_names[Classification.SPAM.value].append(file)

    def save_model(self, file_name, smoothing_value, do_print=False):
        i = 0
        total_vocabulary_words = len(self.vocabulary)
        # total_vocabulary_words += total_vocabulary_words * smoothing_value
        ham_word_count = self.word_count[Classification.HAM.value] + total_vocabulary_words * smoothing_value
        spam_word_count = self.word_count[Classification.SPAM.value] + total_vocabulary_words * smoothing_value
        model = ""
        for word, frequencies in sorted(self.vocabulary.items()):
            i += 1
            ham_word_frequency = self.vocabulary[word][Classification.HAM.value]
            spam_word_frequency = self.vocabulary[word][Classification.SPAM.value]
            model += ("%d  %s  %g  %g  %g  %g\n" % (i, word, ham_word_frequency,
                                                    (ham_word_frequency + smoothing_value) / ham_word_count,
                                                    spam_word_frequency,
                                                    (spam_word_frequency + smoothing_value) / spam_word_count))
        with open(file_name, 'w') as file:
            file.write(model)
        if do_print:
            print(model)

    def test_classify(self, file_name, do_print, smoothing_value):
        file_counter = 0
        num_spam_emails = len(self.file_names[Classification.SPAM.value])
        num_hum_emails = len(self.file_names[Classification.HAM.value])
        total_vocabulary_words = len(self.vocabulary)
        total_vocabulary_words += total_vocabulary_words * smoothing_value
        ham_word_count = self.word_count[Classification.HAM.value] + total_vocabulary_words
        spam_word_count = self.word_count[Classification.SPAM.value] + total_vocabulary_words
        classified_emails = ""
        for i in range(len(self.file_names)):
            classification = Classification(i)
            category = self.file_names[i]
            for document in category:
                file_counter += 1
                path = "test\\"
                path += document
                ham_probability = math.log10(num_hum_emails / (num_spam_emails + num_hum_emails))
                spam_probability = math.log10(num_spam_emails / (num_spam_emails + num_hum_emails))
                data = open(path, "r", encoding="Latin-1")
                for line in data:
                    line = line.lower()
                    line = re.split('[^a-zA-Z]+', line)
                    for word in line:
                        if len(word) == 0:
                            continue
                        if not self.verify_if_stop_word(word) and word in self.vocabulary:
                            ham_word_probability = (self.vocabulary[word][Classification.HAM.value]+smoothing_value)/ham_word_count
                            spam_word_probability = (self.vocabulary[word][Classification.SPAM.value]+smoothing_value)/spam_word_count
                            ham_probability += math.log10(ham_word_probability)
                            spam_probability += math.log10(spam_word_probability)
                if ham_probability > spam_probability:
                    file_classification = Classification.HAM
                else:
                    file_classification = Classification.SPAM
                self.metrics.labeled[file_classification.value] += 1
                self.metrics.total_target[i] += 1
                if file_classification.value != i:
                    right_wrong = "wrong"
                else:
                    self.metrics.correctly[i] += 1
                    right_wrong = "right"
                classified_email = ("%d  %s  %s  %g  %g  %s  %s\n" % (file_counter, document, file_classification.name.lower(),
                                                                      ham_probability, spam_probability,
                                                                      classification.name.lower(), right_wrong))
                classified_emails += classified_email
            with open(file_name, 'a') as file:
                file.write(classified_emails)
            if do_print:
                print(classified_emails.rstrip())
        return file_counter


def task_selection():
    run_again = True
    smoothing_value = 0.5
    while run_again:
        print("=================================================================")
        print("\t\t\t SPAM FILTER - MAIN MENU")
        print("=================================================================")
        print( "Here are your option:\n" +
               "\t 1. Task 1: Building the model \n" +
               "\t 2. Task 2: Building and evaluating the classifier\n" +
               "\t 3. Task 3: Experiment with your Classifier")
        user_input = input("Please choose your task (1-3): ")
        # //////////////TASK 1\\\\\\\\\\\\\\\
        if user_input is "1":
            model = Model()
            print("Running Task 1\n")
            print("Training....")
            model.process_files("train")
            model.process_stop_word("English-Stop-Words.txt")
            model.build_vocabulary(False, False)
            with open('model.txt', 'w') as file:
                file.write('')
            model.save_model('model.txt', 0.5, False)
            print("Training DONE!\n")
            answer = input("would you like to run another task? (y/n): ")
            if answer == "n":
                print("GoodBye")
                run_again = False
        # //////////////TASK 2\\\\\\\\\\\\\\\
        elif user_input is "2":
            model = Model()
            print("Running Task 2\n")
            print("Testing....")
            model.process_files("train")
            model.process_stop_word("English-Stop-Words.txt")
            model.build_vocabulary(False, False)
            model.file_names[Classification.HAM.value].clear()
            model.file_names[Classification.SPAM.value].clear()
            model.process_files("test")
            with open('baseline-result.txt', 'w') as file:
                file.write('')
            model.test_classify('baseline-result.txt', False, smoothing_value)
            print("Testing DONE!\n")
            model.metrics.print_metrics()
            answer = input("would you like to run another task? (y/n): ")
            if answer == "n":
                print("GoodBye")
                run_again = False
        # //////////////TASK 3\\\\\\\\\\\\\\\
        # ~~~~~~~ NOT DONE ~~~~~~~
        elif user_input is "3":
            print("Running task 3: experiments \n")
            experiment_run = True
            while experiment_run:
                u_input = input("which experiment would you like to run? (2 or 3):")
                if u_input == "2":
                    model = Model()
                    print("running Experiment 2 : Stop-word Filtering")
                    model.process_files("train")
                    model.process_stop_word("English-Stop-Words.txt")
                    model.build_vocabulary(True, False)
                    model.save_model('stopword-model.txt', smoothing_value, False)
                    model.file_names[Classification.HAM.value].clear()
                    model.file_names[Classification.SPAM.value].clear()
                    model.process_files("test")
                    model.test_classify('stopword-result.txt', False, smoothing_value)
                    print("Experiment DONE!")
                    model.metrics.print_metrics()
                    answer2 = input("run another experiemnt? (y/n): ")
                    if answer2 == "n":
                        experiment_run = False

                elif u_input == "3":
                    model = Model()
                    print("running Experiment 3 : Word Length Filtering")
                    model.process_files("train")
                    model.process_stop_word("English-Stop-Words.txt")
                    model.build_vocabulary(True, True)
                    model.save_model('wordlength-model.txt', smoothing_value, False)
                    model.file_names[Classification.HAM.value].clear()
                    model.file_names[Classification.SPAM.value].clear()
                    model.process_files("test")
                    model.test_classify('wordlength-result.txt', False, smoothing_value)
                    print("Experiment DONE!")
                    model.metrics.print_metrics()
                    answer2 = input("run another experiemnt? (y/n): ")
                    if answer2 == "n":
                        experiment_run = False

            answer = input("would you like to run another task? (y/n): ")
            if answer == "n":
                print("GoodBye")
                run_again = False


task_selection()
