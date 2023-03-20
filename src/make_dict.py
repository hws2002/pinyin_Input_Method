# make a dict from the file of "拼音汉字表.txt"
# make a dict from the file of "一二级汉字表.txt"
import json

def create_pinyin_char_dict(input_path, valid_chars=None):
    # create dictionary with pinyin keys and empty list values
    pinyin_char_dict = {}
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip().split()
            pinyin = line[0]
            chars = [c for c in line[1:] if c in valid_chars]
            pinyin_char_dict[pinyin] = chars
    f.close()
    return pinyin_char_dict

input_file_path = "../data/拼音汉字表.txt"

with open("../data/一二级汉字表.txt", "r", encoding="utf-8") as f:
    characters = f.read()
    valid_chars = set()
    for c in characters:
        valid_chars.add(c)
f.close()


pinyin_dict = create_pinyin_char_dict(input_file_path,valid_chars)
print(pinyin_dict)


with open("../data/pinyin_dict.txt", 'w', encoding='utf-8') as f:
    json.dump(pinyin_dict, f, ensure_ascii=False, indent=4)
f.close()    
