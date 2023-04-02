import re
import os
import json
import time
#-------------------------------------------------------------#

INPUT_ENCODING = 'gbk'
OUTPUT_ENCODING = 'UTF-8'
CORPORA = "../语料库"

corpora = [
    CORPORA + "/sina_news_gbk/2016-02.txt",
    CORPORA + "/sina_news_gbk/2016-04.txt",
    CORPORA + "/sina_news_gbk/2016-05.txt",
    CORPORA + "/sina_news_gbk/2016-06.txt",
    CORPORA + "/sina_news_gbk/2016-07.txt",
    CORPORA + "/sina_news_gbk/2016-08.txt",
    CORPORA + "/sina_news_gbk/2016-09.txt",
    CORPORA + "/sina_news_gbk/2016-10.txt",
    CORPORA + "/sina_news_gbk/2016-11.txt",
]

chinese_pattern = re.compile('[\u4e00-\u9fff]|[.,，。、！？“”；：""()（）]|\d+')
chinese_character = re.compile('[\u4e00-\u9fff]')
punctuation_mark = {',', '，', '。', '、', '！', '？', '“', '”', '；','：','"',' '}

#-------------------------------------------------------------#
# Any character following after '.' ',' '，', '。' '、' '！' '？' '“' '”' '；'is a first character

draft_dict = {}
draft_dict_first = {}
draft_dict_single = {}

for corpus in corpora:
    filename = os.path.basename(corpus)
    start_time = time.time()
    print(f"pre processing {filename}...")
    with open(corpus, 'r', encoding=INPUT_ENCODING) as f2:
        for line in f2:
            line = line.strip()
            chinese_text = ''.join(chinese_pattern.findall(line))
            if re.match(chinese_character, chinese_text[0]):
                draft_dict_first[chinese_text[0]] = draft_dict_first.get(chinese_text[0],0) + 1
                
            for index,char in enumerate(chinese_text):
                # first character
                if char in punctuation_mark and index+1<len(chinese_text):
                    char2 = chinese_text[index+1]
                    if re.match(chinese_character, char2): 
                        draft_dict_first[char2] = draft_dict_first.get(char2,0) + 1
                    continue
                # single character
                if re.match(chinese_character, char):
                    draft_dict_single[char] = draft_dict_single.get(char, 0) + 1
                    # character pair
                    char2 = chinese_text[index+1] if index+1<len(chinese_text) else ''
                    if re.match(chinese_character, char2):
                        draft_dict[char+char2] = draft_dict.get(char+char2, 0) + 1
        f2.close()
    end_time = time.time()
    print(f"Pre processing {filename} done! Time cost: {end_time-start_time:.2f}s")
# store frequency_dict_first as json file

with open("dict/draft_dict.json", 'w', encoding=OUTPUT_ENCODING) as f:
    json.dump(draft_dict, f, ensure_ascii=False, indent=4)
f.close()

with open("dict/draft_dict_first.json", 'w', encoding=OUTPUT_ENCODING) as f:
    json.dump(draft_dict_first, f, ensure_ascii=False, indent=4)
f.close()

with open("dict/draft_dict_single.json", 'w', encoding=OUTPUT_ENCODING) as f:
    json.dump(draft_dict_single, f, ensure_ascii=False, indent=4)
f.close()

print("Pre Processing1: 'Making Draft Dictionary' Done!")