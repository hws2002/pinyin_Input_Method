import json
import sys
import numpy as np
#----------------------------------------------------------------#
#%% set STRATEGIES
# FDS : frequency_dict_single
# FDF : frequency_dict_first
FIRST_CHAR_STRATEGIES = ["FDS","FDF"]
FIRST_CHAR_STRATEGY = FIRST_CHAR_STRATEGIES[1]

PINYIN_DICT_STRATEGIES = ["SORTED","UNSORTED"]
PINYIN_DICT_STRATEGY = PINYIN_DICT_STRATEGIES[1]

LAMBDA = 0.99
TOP_K = 4
ENCODING = 'gbk'

COUNT_THRESHOLD = 5
SINGLE_COUNT_THRESHOLD = 5
FIRST_COUNT_THRESHOLD = 2

#%% Open dictionaries
if( PINYIN_DICT_STRATEGY == "UNSORTED"):
    with open('../data/pinyin_dict.json', 'r', encoding = ENCODING) as f:
        pinyin_dict = json.load(f)
    f.close()
else :
    with open('../data/pinyin_dict_sorted.json', 'r', encoding = ENCODING) as f:
        pinyin_dict = json.load(f)
    f.close()

with open('../data/frequency_dict.json', 'r', encoding = ENCODING) as f:
    frequency_dict = json.load(f)
f.close()

with open('../data/frequency_dict_single.json', 'r', encoding = ENCODING) as f:
    frequency_dict_single = json.load(f)
f.close()

with open('../data/frequency_dict_first.json', 'r', encoding = ENCODING) as f:
    frequency_dict_first = json.load(f)
f.close()
#----------------------------------------------------------------#

SUM_FREQ_DICT_FIRST = sum(frequency_dict_first.values())
SUM_FREQ_DICT_SINGLE = sum(frequency_dict_single.values())
#%% Define functions
def get_probability_first(char):
    if(FIRST_CHAR_STRATEGY == 'FDF'):
        if char in frequency_dict_first:
            return frequency_dict_first[char] / SUM_FREQ_DICT_FIRST
        else:
            return 1/SUM_FREQ_DICT_FIRST
    else:
        if char in frequency_dict_single:
            return frequency_dict_single[char] / SUM_FREQ_DICT_FIRST
        else :
            return 1/SUM_FREQ_DICT_FIRST

def get_probability(char2, char1=None):
    if(char1) is None:
        if char2 not in frequency_dict_single:
            return 1/SUM_FREQ_DICT_SINGLE
        return frequency_dict_single[char2] / SUM_FREQ_DICT_SINGLE
    else:
        if char1+char2 not in frequency_dict:
            return (1-LAMBDA)*(get_probability(char2))
        else :
            return LAMBDA*(frequency_dict[char1+char2] / frequency_dict_single[char1]) + (1-LAMBDA)*(get_probability(char2))

def transform2sentence(pinyin_line):
    pinyins = pinyin_line.split(' ')
    PROB = np.empty((0,TOP_K), dtype=float)
    TRACE = np.empty((0,TOP_K), dtype=int)
    TOP_CHARACTERS = np.empty((0,TOP_K), dtype=str)
    MAX_PROB = 0

    # TODO : Viterbi algorithm
    
    # handle first character
    char_list1 = pinyin_dict[pinyins[0]]
    first_probabilities = []
    for i,char in enumerate(char_list1):
        first_probabilities.append(-np.log(get_probability_first(char)))
        MAX_PROB = max(MAX_PROB, get_probability_first(char))

    sorted_indices = sorted(range(len(first_probabilities)), key=lambda k: first_probabilities[k], reverse=False)    
    first_probabilities = [first_probabilities[i] for i in sorted_indices]
    char_list1 = [char_list1[i] for i in sorted_indices]
    
    # FOR DEBUGGING
    # print(first_probabilities)
    # print(char_list1)
    
    if len(first_probabilities) > TOP_K:
        first_probabilities = first_probabilities[:TOP_K]
        char_list1 = char_list1[:TOP_K]
    
    PROB = np.append(PROB,[np.pad(first_probabilities,(0,TOP_K-len(first_probabilities)),mode='constant',constant_values =-1)],axis = 0)
    TOP_CHARACTERS = np.append(TOP_CHARACTERS,[np.pad(char_list1,(0,TOP_K-len(char_list1)),mode='constant',constant_values=' ')],axis = 0)
    MAX_PROB = -np.log(MAX_PROB)
    
    # Viterbi
    for i in range(len(pinyins)-1):
        char_list1 = TOP_CHARACTERS[i] # length <= TOP_K
        previous_probs = PROB[i] # length <= TOP_K
        char_list2 = pinyin_dict[pinyins[i+1]] # length could be longer than TOP_K
        
        # FOR DEBUGGING 
        # print(char_list1)
        # print(previous_probs)
        # print(char_list2)
        
        # get_probability : get the probability of char2 given char1        
        best_char_index = []
        max_probabilities = []
        MAX_PROB = sys.maxsize
        for j,char2 in enumerate(char_list2):
            prob = 0
            index = -1
            for i,char1 in enumerate(char_list1):
                if(char1 == ' '):
                    continue
                if prob < get_probability(char2, char1):
                    prob = get_probability(char2, char1)
                    index = i # <= TOP_K
                    
            # Revise best_char_index and max_probabilities
            best_char_index.append(index)
            max_probabilities.append(previous_probs[index]-np.log(prob))
            if (MAX_PROB > max_probabilities[j]):
                MAX_PROB = max_probabilities[j]
        # Revise TRACE, PROB and MAX_PROB
        
        # FOR DEBUGGING
        # print(tracer)
        # print(char_list1[best_char_index[tracer]])
        # print(char_list2[tracer])
        
        # Sort
        sorted_indices = sorted(range(len(max_probabilities)), key=lambda k: max_probabilities[k], reverse=False)
        # print(sorted_indices)
        max_probabilities = [max_probabilities[i] for i in sorted_indices]
        best_char_index = [best_char_index[i] for i in sorted_indices]
        char_list2 = [char_list2[i] for i in sorted_indices]
        
        # Cut off
        if len(best_char_index) > TOP_K:
            best_char_index = best_char_index[:TOP_K]
            max_probabilities = max_probabilities[:TOP_K]
            char_list2 = char_list2[:TOP_K]

        # FOR DEBUGGING
        # print(best_char_index)
        # print(max_probabilities)
        # print(char_list2)
        
        TRACE = np.append(TRACE,[np.pad(best_char_index,(0,TOP_K-len(best_char_index)), mode='constant', constant_values=-1)],axis = 0)
        PROB = np.append(PROB,[np.pad(max_probabilities,(0,TOP_K-len(max_probabilities)),mode='constant',constant_values=-1)],axis = 0)
        TOP_CHARACTERS = np.append(TOP_CHARACTERS,[np.pad(char_list2,(0,TOP_K-len(char_list2)),mode='constant',constant_values=' ')],axis = 0)

    # FOR DEBUGGING
    # print(TOP_CHARACTERS)
    # print(TRACE)
    # print(len(TRACE))
    
    # Backtrace
    len_ = len(pinyins)
    sentence = ''
    tracer = 0
    for i in range(len_-1):
        sentence += TOP_CHARACTERS[len_-i-1][tracer]
        tracer = TRACE[len(pinyins)-i-2][tracer]
    sentence += TOP_CHARACTERS[0][tracer]
    sentence = sentence[::-1]
    print(sentence)
    return sentence

#----------------------------------------------------------------#
# %% Main
# read input file
with open('../test/input.txt','r',encoding = ENCODING) as f:
    input_text = f.read().splitlines()
f.close()

# transform into Chinese sentences and Compare with the original text
with open('../test/my_output.txt','w',encoding = ENCODING) as f:
    for pinyin_line in input_text:
        # print(pinyin_line)
        f.write(transform2sentence(pinyin_line))
        f.write("\n")
f.close()