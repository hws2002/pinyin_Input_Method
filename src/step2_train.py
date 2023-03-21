import json
COUNT_THRESHOLD = 5
training_sets= [
    "../../语料库/sina_news_gbk/cleaned_data/2016-02.txt",
    "../../语料库/sina_news_gbk/cleaned_data/2016-04.txt",
    "../../语料库/sina_news_gbk/cleaned_data/2016-05.txt",
    "../../语料库/sina_news_gbk/cleaned_data/2016-06.txt",
    "../../语料库/sina_news_gbk/cleaned_data/2016-07.txt",
    "../../语料库/sina_news_gbk/cleaned_data/2016-08.txt",
    "../../语料库/sina_news_gbk/cleaned_data/2016-09.txt",
    "../../语料库/sina_news_gbk/cleaned_data/2016-10.txt",
    "../../语料库/sina_news_gbk/cleaned_data/2016-11.txt",
    ]

draft_dict = {}
frequency_dict = {}

with open("../data/pinyin_dict.txt", "r", encoding="gbk") as f:
    characters = f.read()
    valid_chars = set()
    for c in characters:
        valid_chars.add(c)
f.close()

for training_set in training_sets:
    with open(training_set, 'r', encoding='gbk') as f:
        for line in f:
            line = line.strip()
            for i in range(len(line)-1):
                char1 = line[i]
                char2 = line[i+1]
                if char1 in valid_chars and char2 in valid_chars:
                    word = char1+char2
                    if word in draft_dict:
                        draft_dict[word] +=1
                    else:
                        draft_dict[word] = 1
    f.close()

for word in draft_dict:
    if(draft_dict[word] > COUNT_THRESHOLD):
        frequency_dict[word] = draft_dict[word]

#store as json file
with open("../data/frequency_dict.json", 'w', encoding='gbk') as f:
    json.dump(frequency_dict, f, ensure_ascii=False, indent=4)
f.close()    
