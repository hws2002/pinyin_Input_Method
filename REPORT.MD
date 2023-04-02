<font size = "6em" ><bold>**拼音输入法报告** &nbsp;&nbsp;</bold></font> <small>2021080070 计14 韩佑硕 </small> 

# **二元模型介绍以及基本思路**

本实验的任务是实现拼音输入法。即，给定拼音串，要得出合理的汉字字符串。
整个句子S出现的概率为$\prod_{i=1}^{\ n}{P\left(w_i\middle|w_1w_2\ldots w_{i-1}\right)}$而二元模型中，一个汉字确定之后，其下一个汉字所出现的概率只跟这个汉字有关，而跟前面的一些列汉字都无关。（参考 ：https://en.wikipedia.org/wiki/Discrete-time_Markov_chain）  
因此，我们只需算出$\prod_{i=1}^{\ n}{P\left(w_i\middle|w_{i-1}\right)}$且这等价于求$-\sum_{i=1}^{n}{log(P(w_i|w_{i-1}))}$的最小值，

${P\left(w_i\middle|w_{i-1}\right)}$ 为{$w_{i-1}w_i$同现的次数/$w_{i-1}$出现的次数}

# **实验环境**

Anaconda 的虚拟环境

```lua
conda create --name pinyin_method python=3.8
conda activate pinyin_method
```

按照文件名的顺序执行

```python
python3 step1_make_pinyin_dct.py
python3 step2_1_make_draft_dicts.py
python3 step2_2_filter_dicts.py
python3 step3_viterbi.py
python3 step4_evaluation.py
```

即可得到转换结果文件(output.txt)

# **使用语料库和数据预处理方法**

## **使用语料库**

- sina_news_gbk

## **数据预处理方法**

对应的步骤为 step1, step2 

### **STEP1**

#### `step1_make_pinyin_dict.py`  
建立一个 {`拼音`: [汉字列表]}的 dictionary  
INPUT : 拼音汉字表.txt, 一二级汉字表.txt  
OUTPUT : ../dict/pinyin_dict.txt

### **STEP2**

#### `step2_1_make_draft_dicts.py`  
预处理语料库，把html,url,time,title,{}以及各种json格式的key都去掉，只保留汉字，数字和punctuation marks  
是为了统计首个字符。
INPUT : 语料库中的 "2016-0?.txt" 文件
OUTPUT : draft_dict_first.json, draft_dict_single.json, draft_dict.json 分别为首个字符词频表，单个字符的词频表，和双字符的词频表

例子

```text
{"html": "原标题：快讯：台湾高雄6.7级地震 多幢大楼倒塌 不断传出呼救声中国地震台网测定，今日3时57分在台湾高雄市发生6.7级地震。据台媒报道，地震释放能量相当于两颗原子弹。台南市多处楼房倾斜倒塌。其中，台南市永大路二段一栋住宅大楼倒塌，整栋建筑物倒榻在马路上，建筑物内不断传出呼救声。#高雄6.7级地震#", "time": "2016-02-06 06:45", "title": "快讯：台湾高雄6.7级地震 多幢大楼倒塌 不断传出呼救声", "url": "http://news.sina.com.cn/o/2016-02-06/doc-ifxpfhzk9008548.shtml"}
```

变成

```text
"""原标题：快讯：台湾高雄6.7级地震多幢大楼倒塌不断传出呼救声中国地震台网测定，今日3时57分在台湾高雄市发生6.7级地震。据台媒报道，地震释放能量相当于两颗原子弹。台南市多处楼房倾斜倒塌。其中，台南市永大路二段一栋住宅大楼倒塌，整栋建筑物倒榻在马路上，建筑物内不断传出呼救声。高雄6.7级地震","""201602060645","""快讯：台湾高雄6.7级地震多幢大楼倒塌不断传出呼救声","""...201602069008548."
```

#### `step2_2_filter_dicts.py`  
设定THRESHOLD, 建立一个 {`汉字` : `频度`}的 dictionary  
THRESHOLD是储存在dict中汉字的最少出现频度, 可以对三个dict分别设不同THRESHOLD
```python
COUNT_THRESHOLD
SINGLE_COUNT_THRESHOLD
FIRST_COUNT_THRESHOLD
```
INPUT : ../dict/ 中 draft_dict_first.json, draft_dict_single.json, draft_dict.json  
OUTPUT : ../dict/ 中 frequency_dict_first.json, frequency_dict_single.json, frequency_dict.json  

# **训练方法**
使用viterbi算法实现了输入法 
对应步骤为STEP3  
Graph ： 储存List of Node的Graph
Node ： 自定义的class
Node.char ： 该Node的汉字
Node.probability ： P(Node.char | Node.parent.char)
Node.parent ： 用于回溯的 tracer， P(Node.char | Node.parent.char) 为对Node.char来说频率最高的概率

1. 在每一个拼音，先用pinyin_dict找出所可能取到的汉字(States)
2. 对于每个已经筛选的前一层汉字，计算得出probability最高的下一层汉字，并筛选出top TOP_K个 probability
3. 把TOP_K个 probability 对应的Node储存到Graph
4. 回溯Graph得到最终汉字字符串

## **STEP3**
#### `step3_viterbi`
得出最终转换后的汉字字符串  
设置变量为
```python
FIRST_CHAR_STRATEGY
LAMBDA 
TOP_K
ENCODING
```
分别为  
1. 处理首个字符的策略  
2. 平滑参数  
3. 要筛选出的汉字数
4. 编码  

INPUT : step2_2_filter_dicts.py 中的输入 dicts 在 ../dict/, ../data/input.txt  
OUTPUT : ../data中 output.txt 
# **处理方法及效率比较**
对应步骤为STEP4  

## **STEP4**
#### `step4_evaluation.py`  
得出子覆盖率和句覆盖率

## **不同 TOP_K 准确率比较**
LAMBDA = 0.9999999
TOP_K, 字覆盖率，句覆盖率
TOP_K = 3 =>78.63993025283348 % , 21.36006974716652 % 
TOP_K = 4 =>80.73234524847427 % , 19.26765475152572 % 
TOP_K = 5 => 81.67393199651264 % , 18.326068003487357 % 
TOP_K = 6  =>81.84829991281605 % , 18.151700087183958 % 
TOP_K = 7 => 81.88317349607672 % , 18.116826503923278 % 
TOP_K =8 => 81.60418482999128 % , 18.395815170008717 % 



LAMBDA = 0.8
TOP_K = 7 => 82.04010462074979 %, 17.959895379250217 % 
TOP_K = 6 => 82.3539668700959 % ,17.646033129904097 % 

## **例子分析**
### **好的例子**
名牌大学的研究生
### **差的例子**
文言文样例我死了
文言文杨利沃斯勒