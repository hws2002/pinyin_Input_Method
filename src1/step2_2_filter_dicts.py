import json
import sys
import numpy as np
#----------------------------------------------------------------#
#%% set STRATEGIES
# FDS : frequency_dict_single
# FDF : frequency_dict_first
INPUT_ENCODING = 'UTF-8'
OUTPUT_ENCODING = 'gbk'
COUNT_THRESHOLD = 5
SINGLE_COUNT_THRESHOLD = 0
FIRST_COUNT_THRESHOLD = 3

#%% Open dictionaries

with open('../data/draft_dict.json', 'r', encoding = INPUT_ENCODING) as f:
    draft_dict = json.load(f)
f.close()

with open('../data/draft_dict_single.json', 'r', encoding = INPUT_ENCODING) as f:
    draft_dict_single = json.load(f)
f.close()

with open('../data/draft_dict_first.json', 'r', encoding = INPUT_ENCODING) as f:
    draft_dict_first = json.load(f)
f.close()


frequency_dict = {}
frequency_dict_first = {}
frequency_dict_single = {}


for key in draft_dict:
    if draft_dict[key]>=COUNT_THRESHOLD and key in "一二级表":
        frequency_dict[key] = draft_dict[key]

# frequency_dict = dict(sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True))

for key in draft_dict_first:
    if draft_dict_first[key]>=FIRST_COUNT_THRESHOLD:
        frequency_dict_first[key] = draft_dict_first[key]

# frequency_dict_first = dict(sorted(frequency_dict_first.items(), key=lambda x: x[1], reverse=True))

for key in draft_dict_single:
    if draft_dict_single[key]>=SINGLE_COUNT_THRESHOLD:
        frequency_dict_single[key] = draft_dict_single[key]
        
# frequency_dict_single = dict(sorted(frequency_dict_single.items(), key=lambda x: x[1], reverse=True))

with open("../data/frequency_dict.json", 'w', encoding=OUTPUT_ENCODING) as f:
    json.dump(frequency_dict, f, ensure_ascii=False, indent=4)
f.close()

with open("../data/frequency_dict_first.json", 'w', encoding=OUTPUT_ENCODING) as f:
    json.dump(frequency_dict_first, f, ensure_ascii=False, indent=4)
f.close()

with open("../data/frequency_dict_single.json", 'w', encoding=OUTPUT_ENCODING) as f:
    json.dump(frequency_dict_single, f, ensure_ascii=False, indent=4)
f.close()

print("Pre Processing2 : 'filtering dictionaries' Done!")