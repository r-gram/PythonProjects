############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "Robert Gramlich"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.



############################################################
# Section 1: Hidden Markov Models
############################################################

#Load in data 
def load_corpus(path):
    with open(path, 'r') as f:
        lines = []
        for line in f:
            new_line = []
            line_split = line.split()
            for word in line_split:
                word = tuple(word.split('='))
                new_line.append(word)
            lines.append(new_line)
    return lines

class Tagger(object):
    #Use the init function to get start tags, transition probabilites, and emmission probabilities
    def __init__(self, sentences):
        self.tags_POS = ['NOUN', 'VERB', 'ADJ', 'ADV', 'PRON', 'DET', 'ADP', 'NUM', 'CONJ', 'PRT', '.', 'X']
        count_start_POS = {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}
        count_trans_POS = {'NOUN': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'VERB': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'ADJ': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'ADV': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'PRON': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'DET': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'ADP': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'NUM': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'CONJ': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'PRT': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           '.': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'X': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}}
        count_word_tag = {'NOUN': {}, 'VERB': {}, 'ADJ': {}, 'ADV': {}, \
                          'PRON': {}, 'DET': {}, 'ADP': {}, 'NUM': {}, \
                          'CONJ': {}, 'PRT': {}, '.': {}, 'X': {}}
        count_tags = {}
        self.start_prob = {}
        self.trans_prob = {'NOUN': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'VERB': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'ADJ': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'ADV': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'PRON': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'DET': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'ADP': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'NUM': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'CONJ': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'PRT': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           '.': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}, \
                           'X': {'NOUN': 0.0, 'VERB': 0.0, 'ADJ': 0.0, 'ADV': 0.0, 'PRON': 0.0, 'DET': 0.0, 'ADP': 0.0, 'NUM': 0.0, 'CONJ': 0.0, 'PRT': 0.0, '.': 0.0, 'X': 0.0}}
        self.emis_prob = {'NOUN': {}, 'VERB': {}, 'ADJ': {}, 'ADV': {}, \
                          'PRON': {}, 'DET': {}, 'ADP': {}, 'NUM': {}, \
                          'CONJ': {}, 'PRT': {}, '.': {}, 'X': {}}
        
        #Loop through each sentence in the data (we do a lot in this loop) 
        for sen in sentences:
            #Get a count of the tags that start a sentence 
            count_start_POS[sen[0][1]] += 1
            #Look at each (word, tag) in sentence
            for i in range(len(sen)):
                #Count the number of tags in the dataset
                if sen[i][1] in count_tags:
                    count_tags[sen[i][1]] += 1
                else:
                    count_tags[sen[i][1]] = 1
                #Get a count of transitions 
                if i != range(len(sen))[-1]:
                    count_trans_POS[sen[i][1]][sen[i + 1][1]] += 1
                #Add word to tag in count word tag and emission probabilities
                for tag in self.tags_POS:
                    if sen[i][0] not in count_word_tag[tag]:
                        #When a word is encountered add it to the respective dictionary; set all to zero to get proper counts
                        count_word_tag[tag][sen[i][0]] = 0
                        self.emis_prob[tag][sen[i][0]] = 0
                #Count the word tag combos
                count_word_tag[sen[i][1]][sen[i][0]] += 1

        #get start probabilities; use 1/12 for smoothing because it needs to sum to one; if everything was 0 we'd still get 1
        for tag in self.tags_POS:
            start_num = count_start_POS[tag]
            start_den = len(sentences)
            self.start_prob[tag] = (start_num + 1) / (start_den + 12)

        #get transition probabilities; use 1/12 for smoothing because it needs to sum to one; if everything was 0 we'd still get 1
        for tag_i in self.tags_POS:
            trans_den = 0
            for tag_j in self.tags_POS:
                trans_den += count_trans_POS[tag_i][tag_j]
            for tag_j in self.tags_POS:
                trans_num = count_trans_POS[tag_i][tag_j]
                self.trans_prob[tag_i][tag_j] += (trans_num + 1) / (trans_den + 12)

        #get emission probabilities; the denominator for smoothing is how many words there are + 1; add one to account for unknown values
        vocab_smooth = len(count_word_tag['NOUN']) + 1
        for tag in count_word_tag:
            emis_den = count_tags[tag]
            self.emis_prob[tag]['<UNK>'] = 1 / vocab_smooth
            for word in count_word_tag[tag]:
                emis_num = count_word_tag[tag][word]
                self.emis_prob[tag][word] += (emis_num + 1) / (emis_den + vocab_smooth)

    def most_probable_tags(self, tokens):
        #Create a list to store most probable tags
        most_prob_tags = []
        #Look at each word in the tokens
        for word in tokens:
            #Initial best prob and the most prob tag
            best_prob = -1000000
            most_prob_tag = None
            #Loop through every tag to find what word has the highest prob for that tag. Send the highest prob to the list
            for tag in self.tags_POS:
                if word in self.emis_prob[tag]:
                    prob = self.emis_prob[tag][word]
                else:
                    prob = self.emis_prob[tag]['<UNK>']
                if prob >= best_prob:
                    best_prob = prob
                    most_prob_tag = tag
            most_prob_tags.append(most_prob_tag)
        return most_prob_tags

    def viterbi_tags(self, tokens):
        #Create list to store all chains and one to keep track of backpointers
        V = [{}]
        backpointers = [{}]
        #Figure out what tag has the highest prob of being a starter
        for tag in self.tags_POS:
            if tokens[0] in self.emis_prob[tag]:
                V[0][tag] = self.start_prob[tag] * self.emis_prob[tag][tokens[0]]
                backpointers[0][tag] = None
            else:
                V[0][tag] = self.start_prob[tag] * self.emis_prob[tag]['<UNK>']
                backpointers[0][tag] = None
        #loop through each word in the tokens; start at 1 because we already have the start 
        for i in range(1, len(tokens)):
            #Create new dictionaries for the next token in token to track probabilities
            V.append({})
            backpointers.append({})
            #Initial best prob and the most prob tag
            for tag in self.tags_POS:
                max_prob = -1000000
                prev_pointer = None
                #Check the probability of a word having a tag given the previous word
                for prev_state in self.tags_POS:
                    if tokens[i] in self.emis_prob[tag]:
                        curr_V_val = V[i - 1][prev_state] * self.trans_prob[prev_state][tag] * self.emis_prob[tag][tokens[i]]
                    else:
                        curr_V_val = V[i - 1][prev_state] * self.trans_prob[prev_state][tag] * self.emis_prob[tag]['<UNK>']
                    #Check probs to find the highest one
                    if max_prob < curr_V_val:
                        max_prob = curr_V_val
                        prev_pointer = prev_state
                V[i][tag] = max_prob
                backpointers[i][tag] = prev_pointer
        #Find the best state; starting backwards
        best_state = None
        max_prob = -1000000
        for tag in self.tags_POS:
            if max_prob < V[-1][tag]:
                max_prob = V[-1][tag]
                best_state = tag    
        #Get the optimal path; this is done backwards so we need to reverse list at the very end
        optimal_path = []
        t = len(tokens) - 1
        while t != -1:
            optimal_path.append(best_state)    
            best_state = backpointers[t][best_state]
            backpointers.pop()
            t -= 1
        #Get the final result    
        optimal_path.reverse()
        return  optimal_path

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spent about 10 hours on this homework.
"""

feedback_question_2 = """
I found get the initial values to be the most challenging. I got very confused about the last element in a token not getting counted but figure it out.
"""

feedback_question_3 = """
I liked this assignment as a whole. I feel like I learned a lot and found it very interesting.
"""
