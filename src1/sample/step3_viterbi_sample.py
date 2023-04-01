import json
import sys
import numpy as np
#----------------------------------------------------------------#
#%% set STRATEGIES
# FDS : frequency_dict_single
# FDF : frequency_dict_first
FIRST_CHAR_STRATEGIES = ["FDS","FDF"]
FIRST_CHAR_STRATEGY = FIRST_CHAR_STRATEGIES[1]
LAMBDA = 0.999999
NUMBER_OF_ROW = 10
ENCODING = 'gbk'

COUNT_THRESHOLD = 1000
SINGLE_COUNT_THRESHOLD = 500
FIRST_COUNT_THRESHOLD = 200

#%%% Open dictionaries
with open('../../data/pinyin_dict_sorted.json', 'r', encoding = ENCODING) as f:
    pinyin_dict_sorted = json.load(f)
f.close()

with open('../../data/frequency_dict.json', 'r', encoding = ENCODING) as f:
    frequency_dict = json.load(f)
f.close()

with open('../../data/frequency_dict_single.json', 'r', encoding = ENCODING) as f:
    frequency_dict_single = json.load(f)
f.close()

with open('../../data/frequency_dict_first.json', 'r', encoding = ENCODING) as f:
    frequency_dict_first = json.load(f)
f.close()
#----------------------------------------------------------------#

#%% Define functions
def get_probability_first(char):
    if(FIRST_CHAR_STRATEGY == 'FDF'):
        if char in frequency_dict_first:
            return frequency_dict_first[char] / sum(frequency_dict_first.values())
        else:
            # for those characters that do not appear in the first position
            # give them a small probability, which is the same as the probability of a character that appears 200 times
            return FIRST_COUNT_THRESHOLD/sum(frequency_dict_first.values())
    else:
        return frequency_dict_single[char] / sum(frequency_dict_single.values())

def get_probability(char2, char1=None):
    if(char1) is None:
        if char2 not in frequency_dict_single:
            return SINGLE_COUNT_THRESHOLD/sum(frequency_dict_single.values())
        return frequency_dict_single[char2] / sum(frequency_dict_single.values())
    else:
        if char1+char2 not in frequency_dict:
            return (1-LAMBDA)*(get_probability(char2))
        else :
            if char1 in frequency_dict_single:
                return LAMBDA*(frequency_dict[char1+char2] / frequency_dict_single[char1]) + (1-LAMBDA)*(get_probability(char2))
            else :
                return LAMBDA*(frequency_dict[char1+char2] / SINGLE_COUNT_THRESHOLD/sum(frequency_dict_single.values())) + (1-LAMBDA)*(get_probability(char2))



def transform2sentence(pinyin_line):
    pinyins = pinyin_line.split(' ')
    sentence = ''
    RESULT = np.empty((10,1))
    PROB = np.empty((10,1))
    TRACE = np.empty((10,1))
    MAX_PROB = 0
    # TODO : Viterbi algorithm
    
    # handle first character
    char_list1 = pinyin_dict_sorted[pinyins[0]]
    
    for i,char in enumerate(char_list1):
        print(char,"{:.7f}".format(get_probability_first(char)))
        MAX_PROB = max(MAX_PROB, get_probability_first(char))
    RESULT = np.append(RESULT, np.array(char_list1).reshape(-1, 1), axis=1)
    # print(RESULT)
    for i in range(len(pinyins)-1):
        try : 
            char_list2 = pinyin_dict_sorted[pinyins[i+1]]
        except KeyError:
            # 不会发生
            raise Exception(f"Pinyin '{pinyins[i]}' not found in dictionary.")
        print(char_list2)
        
        # get_probability : get the probability of char2 given char1        
        max_probabilities = []
        best_char = []
        max_prob_stage_i = 0
        col1 = PROB[:,i]
        max_prob_trace = 0
        
        for char2 in char_list2:
            prob = 0
            index = -1
            char = ''
            for i,char1 in enumerate(char_list1):
                if prob < get_probability(char2, char1):
                    prob = get_probability(char2, char1)
                    index = i
            try :
                index != -1
            except Exception:
                # 不会发生
                raise Exception(f"Cannot find a best character for '{char2}'. Something went wrong in get_probability().")
            
            best_char.append(index)
            max_probabilities.append(prob)
            if prob*col1[index] > max_prob_stage_i:
                max_prob_stage_i = prob*col1[index]
            # debug
            
        # Revise TRACE, PROB and MAX_PROB
        arr1 = np.array(best_char)
        arr2 = np.array(max_probabilities)
        arr1 = np.pad(arr1,(0,NUMBER_OF_ROW-len(arr1)),mode = 'constant', constant_values = -1)
        arr2 = np.pad(arr2,(0,NUMBER_OF_ROW-len(arr2)),mode = 'constant', constant_values = -1)
        
        TRACE = np.append(TRACE, arr1.reshape(-1, 1), axis=1)
        PROB = np.append(PROB, arr2.reshape(-1, 1), axis=1)
        MAX_PROB = max_prob_stage_i

    print(TRACE)
    # 回溯
    # TODO : backtrace
    
    
    print(sentence)
    return sentence

#----------------------------------------------------------------#
# %% Main
# read input file
with open('../../输入输出格式样例/input copy.txt','r',encoding = ENCODING) as f:
    input_text = f.read().splitlines()
f.close()

# transform into Chinese sentences and Compare with the original text
with open('../../输入输出格式样例/output_sample.txt','w',encoding = ENCODING) as f:
    for pinyin_line in input_text:
        print(pinyin_line)
        f.write(transform2sentence(pinyin_line))
        f.write("\n")
f.close()