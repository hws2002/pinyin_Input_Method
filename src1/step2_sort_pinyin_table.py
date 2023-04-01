import json

ENCODING = 'gbk'
TOP_K = 10

#%% load data
with open('../data/pinyin_dict.json', 'r', encoding = ENCODING) as f:
    pinyin_dict = json.load(f)
f.close()

with open('../data/frequency_dict_single.json', 'r', encoding = ENCODING) as f:
    frequency_dict_single = json.load(f)
f.close()


# %%
PINYIN_TABLE = {}
# sort out & sort chinese characteres in TOP_K
for pinyin in pinyin_dict:
    available_chars = pinyin_dict[pinyin]
    SORTED_OUT_CHARS = []
    for char in available_chars:
        if char in frequency_dict_single:
            SORTED_OUT_CHARS.append(char)
    PINYIN_TABLE[pinyin] = SORTED_OUT_CHARS
    PINYIN_TABLE[pinyin].sort(key=lambda x: frequency_dict_single[x], reverse=True)
    PINYIN_TABLE[pinyin] = PINYIN_TABLE[pinyin][:TOP_K]

for pinyin in PINYIN_TABLE:
    print(pinyin, PINYIN_TABLE[pinyin])
# %% Save processed dictionary
with open("../data/pinyin_dict_sorted.json", 'w', encoding=ENCODING) as f:
    json.dump(PINYIN_TABLE, f, ensure_ascii=False, indent=4)
f.close()