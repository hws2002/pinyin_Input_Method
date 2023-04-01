import json

FIRST_CHAR_STRATEGIES = ["FDS","FDF"]
FIRST_CHAR_STRATEGY = FIRST_CHAR_STRATEGIES[1]
LAMBDA = 0.99999
NUMBER_OF_ROW = 10
ENCODING = 'UTF-8'

with open('../../输入输出格式样例/output_sample.txt','r',encoding = ENCODING) as f1, open('../../输入输出格式样例/std_output.txt','r',encoding=ENCODING) as f2:
    myoutput = f1.read()
    stdoutput = f2.read()
f1.close()
f2.close()

# %%
def evaluation(my,std):
    deno = 0
    correct = 0
    for i in range(len(std)):
        deno += len(std[i])
        for j in range(len(std[i])):
            if my[i][j] == std[i][j]:
                correct += 1
    
    return (correct*100.0/deno)
#%%

print("字覆盖率为",evaluation(myoutput,stdoutput),"% !")
