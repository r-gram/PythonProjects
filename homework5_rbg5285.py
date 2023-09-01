############################################################
# CMPSC442: Homework 5
############################################################

student_name = "Robert Gramlich"

############################################################
# Imports
############################################################

import email
from math import log
from os import listdir

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    #Open file first and set enconding to utf-8 to fix some code error
    file = open(email_path, 'r', encoding = 'utf-8')
    #Get the body of the email from the file
    e_message = email.message_from_file(file)
    #Make each line in the email an iterator
    m_lines = email.iterators.body_line_iterator(e_message)
    #Create a list of words from the given email file
    word_list = []

    #Iterate over each line, split it by whitespaces, add each word to the list 
    for word in m_lines:
        word_list += word.split()
    return word_list

def log_probs(email_paths, smoothing):
    #Dictionary that function will return containing log probs
    log_prob_dic = {}
    #List that contains all the words from the given emails
    all_words = []
    #Dictionary that contains all word counts from the given emails 
    total_word_count = {}

    #Get all the words from the given emails and add to a list
    for paths in email_paths:
        all_words += load_tokens(paths)

    #Count how many times a word appears in the given emails 
    for word in all_words:
        if word in total_word_count:
            total_word_count[word] += 1
        else: 
            total_word_count[word] = 1

    #Get count of all words
    count_total = 0
    for words in total_word_count:
        count_total += total_word_count[words]

    #Get the vocabulary, the number of unique words in all the emails
    V = len(total_word_count)
    
    #We want the log prob of each unique word so we iterate over the dictionary to avoid duplicates
    for word in total_word_count:
        count_w = total_word_count[word]
        w_numerator = count_w + smoothing
        w_denominator = count_total + (smoothing * (V + 1))
        log_prob_word = log(w_numerator / w_denominator)
        log_prob_dic[word] = log_prob_word
    #Now to get the log prob for unknown
    u_numerator = smoothing 
    u_denominator = count_total + (smoothing * (V + 1))
    log_prob_unk = log(u_numerator / u_denominator)
    log_prob_dic['<UNK>'] = log_prob_unk

    return log_prob_dic


class SpamFilter(object):
    def __init__(self, spam_dir, ham_dir, smoothing):
        #Get all the files in the given ham and spam directory
        spam_files = [spam_dir + '/' + file for file in listdir(spam_dir)]
        ham_files = [ham_dir + '/' + file for file in listdir(ham_dir)]

        #Create list of words for ham and spam 
        #Create dicitionarie of word counts for ham and spam
        spam_words = []
        ham_words = []
        spam_dict = {}
        ham_dict = {}
        for path in spam_files:
            spam_words += load_tokens(path)
        for path in ham_files:
            ham_words += load_tokens(path)
        for word in spam_words:
            if word in spam_dict:
                spam_dict[word] += 1
            else:
                spam_dict[word] = 1
        for word in ham_words:
            if word in ham_dict:
                ham_dict[word] += 1
            else:
                ham_dict[word] = 1

        #Get word count dictionary for ham and spam
        self.wordcount_spam = spam_dict
        self.wordcount_ham = ham_dict
        
        #Compute the log probs for all the words in all the ham and spam files 
        self.logprob_dic_spam = log_probs(spam_files, smoothing)
        self.logprob_dic_ham = log_probs(ham_files, smoothing)

        #Compute class probs of ham and spam based off the number of files in the input directory
        self.prob_spam = len(spam_files) / (len(spam_files) + len(ham_files))
        self.prob_ham = len(ham_files) / (len(spam_files) + len(ham_files))

    def is_spam(self, email_path):
        #Get the log of prob_spam and prob_ham so that calculation are done in logspace
        log_prob_spam = log(self.prob_spam)
        log_prob_ham = log(self.prob_ham)
        #Create a dictionary for spam and ham based off the given doc
        given_email_words_spam = {}
        given_email_words_ham = {}

        #Loop through every word in the given doc and check it against the spam set 
        #First check if the word is in the train set and change that word to unknown if it's not
        #If the word is in the train set then add its count to the dict
        for word in load_tokens(email_path):
            if word not in self.logprob_dic_spam:
                if '<UNK>' in given_email_words_spam:
                    given_email_words_spam['<UNK>'] += 1
                else:
                    given_email_words_spam['<UNK>'] = 1
            else:
                if word in given_email_words_spam:
                    given_email_words_spam[word] += 1
                else:
                    given_email_words_spam[word] = 1
        #Loop through every word in the given doc and check it against the ham set 
        #First check if the word is in the train set and change that word to unknown if it's not
        #If the word is in the train set then add its count to the dict
        for word in load_tokens(email_path):
            if word not in self.logprob_dic_ham:
                if '<UNK>' in given_email_words_ham:
                    given_email_words_ham['<UNK>'] += 1
                else:
                    given_email_words_ham['<UNK>'] = 1
            else:
                if word in given_email_words_ham:
                    given_email_words_ham[word] += 1
                else:
                    given_email_words_ham[word] = 1
        
        #Get the log probabilty for whether the doc is spam
        #Get prob by doing log(P(spam|doc)) = log(P(spam) * P(w|spam)**count(w))
        for word in given_email_words_spam:
            log_prob_spam += given_email_words_spam[word] * self.logprob_dic_spam[word]
        #Get the log probabilty for whether the doc is ham
        #Get prob by doing log(P(ham|doc)) = log(P(ham) * P(w|ham)**count(w))
        for word in given_email_words_ham:
            log_prob_ham += given_email_words_ham[word] * self.logprob_dic_ham[word]
        
        #if the log prob of spam is greater than the log prob of ham then the document is spam
        if log_prob_spam > log_prob_ham:
            return True
        else:
            return False

    def most_indicative_spam(self, n):
        #Create a list of the n most indicative words
        best_n = []
        #Create a list of all words with their log prob
        spam_ind_list = []
        total_wc = {}
        total_words = 0

        #Find words that are in both spam and ham
        #If a word is in both we add its total word count from both spam and ham and create a dict entry for it 
        for word in self.wordcount_spam:
            if word in self.wordcount_ham:
                if word in total_wc:
                    tot = self.wordcount_spam[word] + self.wordcount_ham[word]
                    total_wc[word] += tot
                else:
                    tot = self.wordcount_spam[word] + self.wordcount_ham[word]
                    total_wc[word] = tot
        
        #Get the total count of all the words 
        for word in total_wc:
            total_words += total_wc[word]
        
        #We now compute the log probs for each word with how indicative it is that its spam
        for word in total_wc:
            prob_w = total_wc[word] / total_words
            log_prob_w = log(prob_w)
            log_ind_val = self.logprob_dic_spam[word] - log_prob_w
            spam_ind_list.append((log_ind_val, word))
        
        #This finds the n best indicative values
        for i in range(n):
            best_n.append(max(spam_ind_list)[1])
            spam_ind_list.remove(max(spam_ind_list))

        return best_n

    def most_indicative_ham(self, n):
        #Create a list of the n most indicative words
        best_n = []
        #Create a list of all words with their log prob
        ham_ind_list = []
        total_wc = {}
        total_words = 0

        #Find words that are in both spam and ham
        #If a word is in both we add its total word count from both spam and ham and create a dict entry for it 
        for word in self.wordcount_ham:
            if word in self.wordcount_spam:
                if word in total_wc:
                    tot = self.wordcount_ham[word] + self.wordcount_spam[word]
                    total_wc[word] += tot
                else:
                    tot = self.wordcount_ham[word] + self.wordcount_spam[word]
                    total_wc[word] = tot

        #Get the total count of all the words
        for word in total_wc:
            total_words += total_wc[word]
 
        #We now compute the log probs for each word with how indicative it is that its ham
        for word in total_wc:
            prob_w = total_wc[word] / total_words
            log_prob_w = log(prob_w)
            log_ind_val = self.logprob_dic_ham[word] - log_prob_w
            ham_ind_list.append((log_ind_val, word))
   
        #This finds the n best indicative values
        for i in range(n):
            best_n.append(max(ham_ind_list)[1])
            ham_ind_list.remove(max(ham_ind_list))

        return best_n

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spent about 15 hours on this assignment.
"""

feedback_question_2 = """
I found the log probs part to be the most challenging. This was only the case because of some confusion with given hints.
There were no obvious stumbling blocks because the confusion only lasted for about an hour. 
"""

feedback_question_3 = """
I enjoyed the whole assignment. I felt like I learned a lot while doing. The in-class examples and coding exercises really helped. 
"""