import json

def create_pinyin_char_dict(input_path, valid_chars):
    # create dictionary with pinyin keys and empty list values
    pinyin_char_dict = {}
    l_pinyin = ''
    length_ = 0
    with open(input_path, 'r', encoding='gbk') as f:
        for line in f:
            line = line.strip().split()
            pinyin = line[0]
            chars = [c for c in line[1:] if c in valid_chars]
            pinyin_char_dict[pinyin] = chars
            if len(chars) > length_:
                length_ = len(chars)
                l_pinyin = pinyin
    f.close()
    return pinyin_char_dict,l_pinyin,length_

input_file_path = "dict/拼音汉字表.txt"

with open("dict/一二级汉字表.txt", "r", encoding="gbk") as f:
    characters = f.read()
    valid_chars = set()
    for c in characters:
        valid_chars.add(c)
f.close()

pinyin_dict,l_pinyin, length_ = create_pinyin_char_dict(input_file_path,valid_chars)
print(pinyin_dict)
print(l_pinyin)
print(length_)

#store as json file
with open("dict/pinyin_dict.json", 'w', encoding='gbk') as f:
    json.dump(pinyin_dict, f, ensure_ascii=False, indent=4)
f.close()    
#store as txt file
with open("dict/pinyin_dict.txt", 'w', encoding='gbk') as f:
    for key, value in pinyin_dict.items():
        f.write(' '.join(value))
f.close()