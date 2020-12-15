from nltk.tokenize import sent_tokenize, word_tokenize 
from collections import Counter
from math import log2

def slicer(my_str,sub):
    index=my_str.find(sub)
    if index !=-1 :
        return my_str[:index] 
    else :
        raise Exception('Sub string not found!')

file1 = open('/home/kali/Documents/Github/halstead-metrics/input2.txt',  encoding="utf8")
Lines1 = file1.readlines() 

tokens_op=[]
word_tokens = []

for line in Lines1:
    if line.startswith('/*') or line.startswith('*') or line.startswith('//'):
        continue  # skip comments
        #line = line.replace(line," ")
    tokens_op.append(sent_tokenize(line))

for op in range(0,len(tokens_op)):
    if "//" in tokens_op[op][0]:
        tokens_op[op][0]=(slicer(tokens_op[op][0],"//"))
    word_tokens.append(word_tokenize(tokens_op[op][0]))

print(word_tokens)    

for op in range(0,len(word_tokens)):

    if ("i++" in word_tokens[op]) or ("j++" in word_tokens[op]):
        x = [i.split('++') for i in word_tokens[op]]
        word_tokens[op] = [j for i in x for j in i]
        word_tokens[op] = ["++" if x == '' else x for x in word_tokens[op]]        

    if "``" in word_tokens[op]:
        index = [i.find("``") and i.find("''") for i in word_tokens[op]] # "''" thats probably cuz of a typo... 
        item=[]
        for j in range(0,len(index)):
            if index[j]==0:
                item.append(j)        
        y = [''.join(word_tokens[op][item[0]:item[1]+1])]
        for i in range(item[0], item[1]+1):
            word_tokens[op][i]=slicer(word_tokens[op][i],str(word_tokens[op][i]))
        word_tokens[op][item[0]:item[1]] = ''.join(word_tokens[op][item[0]:item[1]+1])
        word_tokens[op][item[0]] = y[0]
    
    if "[" in word_tokens[op] and "]" in word_tokens[op]:
        index = [i.find("[") and i.find("]") for i in word_tokens[op]]
        item=[]
        for j in range(0,len(index)):
            if index[j]==0:
                item.append(j)     
        count = int((len(item)/2 - 1)*2)
        
        if count == 2: # you may need to add cases ... it should take values (*2) ...
            myorderlist = []
            for i in range(0,item[0]+1):
                myorderlist.append(i)
            myorderlist.append(item[1])
            for i in range(item[0],item[1]+1):
                if i not in myorderlist: myorderlist.append(i)
            for i in range(item[1],item[2]+1):
                if i not in myorderlist: myorderlist.append(i)
            myorderlist.append(item[3])
            for i in range(item[2],len(word_tokens[op])):
                if i not in myorderlist:  myorderlist.append(i)
            word_tokens[op] = [word_tokens[op][i] for i in myorderlist]
        else:
            myorderlist = []
            for i in range(0,item[0]+1):
                myorderlist.append(i)
            myorderlist.append(item[1])
            for i in range(item[0],item[1]+1):
                if i not in myorderlist: myorderlist.append(i)
            for i in range(item[1],len(word_tokens[op])):
                if i not in myorderlist:  myorderlist.append(i)
            word_tokens[op] = [word_tokens[op][i] for i in myorderlist]
        index = [i.find("[") and i.find("]") for i in word_tokens[op]]
        item=[]
        for j in range(0,len(index)):
            if index[j]==0:
                item.append(j)   
        count = int((len(item)/2 - 1)*2)
        
        if count == 2: # you may change that... it takes values (*2) ...
            while count >= 0:
                y = [''.join(word_tokens[op][item[count]-1:item[count+1]+1])]
                for i in range(item[count], item[count+1]+1):
                    word_tokens[op][i]=slicer(word_tokens[op][i],str(word_tokens[op][i]))     
                word_tokens[op][item[count]-1:item[count+1]+1] = ''.join(word_tokens[op][item[count]-1:item[count+1]+1])
                word_tokens[op][item[count]-1] = y[0]
                count -= 2
        else:
            y = [''.join(word_tokens[op][item[count]-1:item[count+1]+1])]
            for i in range(item[count], item[count+1]+1):
                word_tokens[op][i]=slicer(word_tokens[op][i],str(word_tokens[op][i]))
            word_tokens[op][item[count]-1:item[count+1]+1] = ''.join(word_tokens[op][item[count]-1:item[count+1]+1])
            word_tokens[op][item[count]-1] = y[0]  

    if "(" in word_tokens[op] and ")" in word_tokens[op]:
        index = [i.find("(") and i.find(")") for i in word_tokens[op]]
        item=[]
        for j in range(0,len(index)):
            if index[j]==0:
                item.append(j)     
        count = int((len(item)/2 - 1)*2)
        myorderlist = []
        for i in range(0,item[0]+1):
            myorderlist.append(i)
        myorderlist.append(item[1])
        for i in range(item[0],item[1]+1):
            if i not in myorderlist: myorderlist.append(i)
        
        for i in range(item[1],len(word_tokens[op])):
            if i not in myorderlist:  myorderlist.append(i)
        word_tokens[op] = [word_tokens[op][i] for i in myorderlist]
        y = [''.join(word_tokens[op][item[count]-1:item[count]+2])]
        
        for i in range(item[count]-1, item[count]+2):
            word_tokens[op][i]=slicer(word_tokens[op][i],str(word_tokens[op][i]))
        word_tokens[op][item[count]:item[count]+2] = ''.join(word_tokens[op][item[count]-1:item[count]+2])
        word_tokens[op][item[count]-1] = y[0]  

x = [i for i in word_tokens]
word_tokens = [j for i in x for j in i]
print(word_tokens)
word_counter = Counter(word_tokens)
print(word_counter)
#Define operators lexico`
operators = ["{","}",",",";","+","++","--","-","*","/","<",">","<=",">=","for()","while()","do","if()","else","return","=","==","byte","char","short","int","long","float","double","scanf()","&","a[]"]    

index_n1 = []
index_N1 = []
index_N2 = word_tokens

for i in range(0, len(operators)):
    if operators[i] in word_tokens:
        index_n1.append(operators[i])
print(index_n1[5])
for i in range(0, len(word_tokens)):
    if word_tokens[i] in operators:
        index_N1.append(word_tokens[i])
for i in range(0,len(index_n1)):
    while index_n1[i] in index_N2:
        index_N2.remove(str(index_n1[i]))

#############################################################################
#           HALSTEAD METRICS                                                #
#############################################################################

n2 = len(Counter(index_N2))
N2 = len(index_N2)
n1 = len(index_n1)
N1 = len(index_N1)

val = {"n1": n1, "N1": N1, "n2": n2, "N2": N2, "N": N1 + N2, "n": n1 + n2, "V": round((N1 + N2) * log2(n1 + n2),2), "D": round(n1 * N2 / 2 / n2,2)}
val['E'] = round(val['D'] * val['V'],2)
val['L'] = round(val['V'] / val['D'] / val['D'],2)
val['I'] = round(val['V'] / val['D'],2)
val['T'] = round(val['E'] / (18),2)
val['N^'] = round(n1 * log2(n1) + n2 * log2(n2),2)
val['L^'] = round(2 * n2 / N2 / n1,2)

unit = {'V': 'bits', 'T': 'seconds'}
name = {'n1':'n1','N1':'N1','n2':'n2','N2':'N2','N':'Halstead Program Length', 'n':'Halstead Vocabulary', 'V':'Program Volume', 'D':'Program Difficulty', 'E': 'Programming Effort', 'L':'Language level', 'I':'Intelligence Content', 'T':'Programming time','N^':'Estimated program length', 'L^':'Estimated language level'}

print("\nThe various values are: ")
for key in val.keys():
    print("{} ({}) = {} {}".format(key,name[key], val[key], unit[key] if key in unit else ''))