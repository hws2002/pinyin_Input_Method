import re
import os

training_sets = [
    "../../语料库/sina_news_gbk/2016-02-sample.txt",
    "../../语料库/sina_news_gbk/2016-04-sample.txt",
    ]

chinese_pattern = re.compile('[\u4e00-\u9fff]+')

    
    
for training_set in training_sets[0:1]:
    filename = os.path.basename(training_set)
    print(f"pre processing {filename}...")
    with open(f'../../语料库/sina_news_gbk/cleaned_data/{filename}','w',encoding='gbk') as f1:
        with open(training_set, 'r', encoding='gbk') as f2:
            for line in f2:
                line = line.strip()
                chinese_text = ''.join(chinese_pattern.findall(line))
                print(chinese_text[0:3])
                if chinese_text[0:3] == '原标题':
                    f1.write(chinese_text[3:])
                else:
                    f1.write(chinese_text)
                f1.write('\n')
            f2.close()
        f1.close()
