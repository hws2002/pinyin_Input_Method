import json

FIRST_CHAR_STRATEGIES = ["FDS","FDF"]
FIRST_CHAR_STRATEGY = FIRST_CHAR_STRATEGIES[1]
LAMBDA = 0.99999
NUMBER_OF_ROW = 10
ENCODING = 'gbk'

with open('../data/output.txt','r',encoding = ENCODING) as f1, open('../data/std_output.txt','r',encoding=ENCODING) as f2:
    myoutput = f1.read()
    stdoutput = f2.read()
f1.close()
f2.close()

# %%
def evaluation_word(my,std):
    deno = 0
    correct = 0
    for i in range(len(std)):
        deno += len(std[i])
        for j in range(len(std[i])): 
            if my[i][j] == std[i][j]:
                correct += 1
    
    return (correct*100.0/deno)
def evaluation_sentence(my,std):
    deno = 0
    correct = 0
    for line1, line2 in zip(my, std):
        deno += 1
        if line1 != line2:
            correct+=1
            
    return (correct*100.0/deno)
#%%

print("字覆盖率为",evaluation_word(myoutput,stdoutput),"% !")
print("句覆盖率为",evaluation_sentence(myoutput,stdoutput),"% !")