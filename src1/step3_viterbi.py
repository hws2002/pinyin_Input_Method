import json

#----------------------------------------------------------------#
# STRATEGIES
# FDS : frequency_dict_single
# FDF : frequency_dict_first
FIRST_CHAR_STRATEGIES = ["FDS","FDF"]
FIRST_CHAR_STRATEGY = FIRST_CHAR_STRATEGIES[1]
TOP_K = 8
LAMBDA = 0.8
ENCODING = 'gbk'

# bigram model
with open('../data/pinyin_dict.json', 'r', encoding = ENCODING) as f:
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

def get_probability_first(char):
    if(FIRST_CHAR_STRATEGY == 'FDF'):
        return frequency_dict_first[char] / sum(frequency_dict_first.values())
    else:
        return frequency_dict_single[char] / sum(frequency_dict_single.values())
    

def get_probability(char2, char1=None):
    if(char1) is None:
        return frequency_dict_single[char2] / sum(frequency_dict_single.values())
    else:
        return LAMBDA*(frequency_dict[char1+char2] / frequency_dict_single[char1]) + (1-LAMBDA)*(get_probability(char2))



def transform2sentence(pinyin_line):
    pinyins = pinyin_line.split(' ')
    for i in range(len(pinyins)-1):
        try :
            available_char1 = pinyin_dict[pinyins[i]]
            available_char2 = pinyin_dict[pinyins[i+1]]
        except KeyError:
            raise Exception(f"Pinyin '{pinyins[i]}' not found in dictionary.")
        pinyin2chinese(available_char1,available_char2)



#----------------------------------------------------------------#

# read input file
with open('../test/input.txt','r',encoding = ENCODING) as f:
    input_text = f.read().splitlines()
f.close()

# transform into Chinese sentences and Compare with the original text
with open('../test/output.txt','w',encoding = ENCODING) as f:
    for pinyin_line in input_text:
        f.write(transform2sentence(pinyin_line))
        f.write("\n")
    


