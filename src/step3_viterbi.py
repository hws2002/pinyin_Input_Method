import json
import math
#----------------------------------------------------------------#
#%% set STRATEGIES
# FDS : frequency_dict_single
# FDF : frequency_dict_first
FIRST_CHAR_STRATEGIES = ["FDS","FDF"]
FIRST_CHAR_STRATEGY = FIRST_CHAR_STRATEGIES[1]

LAMBDA = 0.8
TOP_K = 8
ENCODING = 'gbk'

#%% Open dictionaries

with open('dict/pinyin_dict.json', 'r', encoding = ENCODING) as f:
    pinyin_dict = json.load(f)
f.close()

with open('dict/frequency_dict.json', 'r', encoding = ENCODING) as f:
    frequency_dict = json.load(f)
f.close()

with open('dict/frequency_dict_single.json', 'r', encoding = ENCODING) as f:
    frequency_dict_single = json.load(f)
f.close()

with open('dict/frequency_dict_first.json', 'r', encoding = ENCODING) as f:
    frequency_dict_first = json.load(f)
f.close()
#----------------------------------------------------------------#


SUM_FREQ_DICT_FIRST = sum(frequency_dict_first.values())
SUM_FREQ_DICT_SINGLE = sum(frequency_dict_single.values())
#%% Define functions
def get_frequency_first(char):
    if(FIRST_CHAR_STRATEGY == 'FDF'):
        if char in frequency_dict_first:
            return frequency_dict_first[char]
        else:
            return 1
    else:
        if char in frequency_dict_single:
            return frequency_dict_single[char]
        else :
            return 1

def get_frequency_single(char):
    if char in frequency_dict_single:
        return frequency_dict_single[char]
    else:
        return 1


def get_frequency(char1, char2):
    if char1+char2 in frequency_dict:
        return frequency_dict[char1+char2]
    else:
        return 1

def get_probability(char1,char2):
    return -math.log(LAMBDA*get_frequency(char1,char2)/get_frequency_single(char1) + (1-LAMBDA)*get_frequency_single(char2)/SUM_FREQ_DICT_SINGLE)
    
class Node:
    def __init__(self, char:str, probability=math.inf, parent=None):
        self.char = char
        self.probability = probability
        self.parent = parent
    def __lt__(self, other):
        return self.probability < other.probability
    def __gt__(self, other):
        return self.probability > other.probability

# Viterbi Algorithm
def transform2sentence(pinyin_line):
    pinyins = pinyin_line.split(' ')
    Graph = []
    
    # handle first character
    char_list2 = pinyin_dict[pinyins[0]]
    char_list2.sort(key = get_frequency_first, reverse = True)
    
    Nodes = []
    for i in range(min(TOP_K,len(char_list2))):
        Nodes.append(Node(char_list2[i], -math.log(get_frequency_first(char_list2[i])/SUM_FREQ_DICT_FIRST)))
        
    Graph.append(Nodes)
    
    # Viterbi
    for i in range(1, len(pinyins)):
        prev_nodes = Graph[i-1]
        char_list2  = pinyin_dict[pinyins[i]]
        # get the probability of char2 given char1        
        Nodes = []
        for char2 in char_list2:
            Nodes.append(Node(char2))
            
        for prev_node in prev_nodes:
            for node in Nodes:
                prob = prev_node.probability + get_probability(prev_node.char, node.char)
                if prob < node.probability:
                    node.probability = prob
                    node.parent = prev_node
        # Sort
        Nodes.sort(key = lambda x : x.probability)
        Nodes = Nodes[:TOP_K]
        Graph.append(Nodes)
    
    
    # Backtrace
    
    sentence = ''
    tracer = min(Graph[len(pinyins)-1])
    sentence += tracer.char
    for i in range(len(pinyins)-1):
        tracer = tracer.parent
        sentence = tracer.char + sentence
    print(sentence)
    return sentence

#----------------------------------------------------------------#
# %% Main
# read input file
with open('../data/input.txt','r',encoding = ENCODING) as f:
    input_text = f.read().splitlines()
f.close()

# transform into Chinese sentences and Compare with the original text
with open('../data/output.txt','w',encoding = ENCODING) as f:
    for pinyin_line in input_text:
        # print(pinyin_line)
        f.write(transform2sentence(pinyin_line))
        f.write("\n")
f.close()