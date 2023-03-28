import json

#----------------------------------------------------------------#
# STRATEGIES
# FDS : frequency_dict_single
# FDF : frequency_dict_first
FIRST_CHAR_STRATEGIES = ["FDS","FDF"]
FIRST_CHAR_STRATEGY = FIRST_CHAR_STRATEGIES[1]
TOP_K = 4
LAMBDA = 0.8
ENCODING = 'gbk'

COUNT_THRESHOLD = 1000
SINGLE_COUNT_THRESHOLD = 500
FIRST_COUNT_THRESHOLD = 200

# bigram model
with open('../../data/pinyin_dict.json', 'r', encoding = ENCODING) as f:
    pinyin_dict = json.load(f)
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

def get_probability_first(char):
    if(FIRST_CHAR_STRATEGY == 'FDF'):
        return frequency_dict_first[char] / sum(frequency_dict_first.values())
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


def pinyin2Chinese(char_list1, char_list2):
    res = ''
    max_prob = 0
    for char1 in char_list1:
        for char2 in char_list2:
            if max_prob < get_probability(char2, char1):
                max_prob = get_probability(char2, char1)
                res = char1 + char2
    try:
        len(res) == 2
    except Exception:
        raise Exception(f"Cannot find a word for pinyin")    
    return res

def transform2sentence(pinyin_line):
    pinyins = pinyin_line.split(' ')
    sentence = ''
    for i in range(len(pinyins)-1):
        try :
            available_char1 = pinyin_dict[pinyins[i]]
            available_char2 = pinyin_dict[pinyins[i+1]]
        except KeyError:
            raise Exception(f"Pinyin '{pinyins[i]}' not found in dictionary.")
        sentence += pinyin2Chinese(available_char1,available_char2)
        print(sentence)
    return sentence

#----------------------------------------------------------------#

# read input file
with open('../../输入输出格式样例/input.txt','r',encoding = ENCODING) as f:
    input_text = f.read().splitlines()
f.close()

# transform into Chinese sentences and Compare with the original text
with open('../../输入输出格式样例/output_sample.txt','w',encoding = ENCODING) as f:
    for pinyin_line in input_text:
        print(pinyin_line)
        f.write(transform2sentence(pinyin_line))
        f.write("\n")
f.close()




