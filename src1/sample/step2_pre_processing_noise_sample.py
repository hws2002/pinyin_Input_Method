import re
import os
import json
#-------------------------------------------------------------#

SINGLE_COUNT_THRESHOLD = 0
FIRST_COUNT_THRESHOLD = 0
corpora = [
    "../../语料库/sina_news_gbk/sample/2016-02 sample.txt",
]

chinese_pattern = re.compile('[\u4e00-\u9fff]|[.,，。、！？“”；：""]|\d+')
chinese_character = re.compile('[\u4e00-\u9fff]')
punctuation_mark = {',', '，', '。', '、', '！', '？', '“', '”', '；','：','"',' '}

#-------------------------------------------------------------#

# TODO : Make "frequency_dict_first"
# Any character following after '.' ',' '，', '。' '、' '！' '？' '“' '”' '；'is a first character
# TODO : Make "frequency_dict_single"
draft_dict_first = {}
draft_dict_single = {}
frequency_dict_first = {}
frequency_dict_single = {}

for corpus in corpora:
    filename = os.path.basename(corpus)
    print(f"pre processing {filename}...")
    with open(f'../../语料库/sina_news_gbk/cleaned_data/sample/{filename}','w',encoding='utf-8') as f1:
        with open(corpus, 'r', encoding='utf-8') as f2:
            for line in f2:
                line = line.strip()
                chinese_text = ''.join(chinese_pattern.findall(line))
                if re.match(chinese_character, chinese_text[0]):
                    draft_dict_first[chinese_text[0]] = draft_dict_first.get(chinese_text[0],0) + 1
                for index,char in enumerate(chinese_text):
                    if char in punctuation_mark and index+1<len(chinese_text):
                        char = chinese_text[index+1]
                        if re.match(chinese_character, char): 
                            draft_dict_first[char] = draft_dict_first.get(char,0) + 1
                        continue
                    if re.match(chinese_character, char):
                        draft_dict_single[char] = draft_dict_single.get(char, 0) + 1
                f1.write(chinese_text)
                f1.write('\n')
            f2.close()
        f1.close()


for key in draft_dict_first:
    if draft_dict_first[key]>=FIRST_COUNT_THRESHOLD:
        frequency_dict_first[key] = draft_dict_first[key]

for key in draft_dict_single:
    if draft_dict_single[key]>=SINGLE_COUNT_THRESHOLD:
        frequency_dict_single[key] = draft_dict_single[key]
        
# store frequency_dict_first as json file
with open("../data/sample/frequency_dict_first_sample.json", 'w', encoding='utf-8') as f:
    json.dump(frequency_dict_first, f, ensure_ascii=False, indent=4)
f.close()

with open("../data/sample/frequency_dict_single_sample.json", 'w', encoding='utf-8') as f:
    json.dump(frequency_dict_single, f, ensure_ascii=False, indent=4)
f.close()