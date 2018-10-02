#encoding:utf-8  
  
from time import time  
  
words = [  
'fuck',  
]  
   
#wordTree = wordTree.append(0)  
   
def create_word_tree(words_list):  
    wordTree = [None for i in range(0,256)]  
    wordTree = [wordTree,0]  
    for word in words_list:  
   
        # 每个单词对应一个tree  
        tree = wordTree[0]  
        for i  in range(0,len(word)):  
            little = word[i]  
            index = ord(little)  
            # 已经到最后一个字母了  
            if i ==  len(word) -1:  
                tree[index] = 1  
            else:  
                tree[index] = [[None for x in range(0,256)],1]  
                tree = tree[index][0]  
   
    return wordTree  
   
def translate(string,tree):  
    temp = tree  
    result = ''  
    for little in string:  
        index = ord(little)  
        temp = temp[0][index]  
        if temp == None:  
            temp = tree  
            #print 'can not find'  
        else:  
            result += chr(index)  
        if temp == 1:   
            return string.replace(result,'')   
  


tree = create_word_tree(words)  
fileP = open('C:/Users/Administrator/Desktop/test.txt')  
s = fileP.read()  
beginTime = time()  
s2 = translate(s,tree)  
endTime = time()  
  
print(endTime - beginTime)  
fileQ = open('C:/Users/Administrator/Desktop/test_result2.txt', 'w')  
fileQ.write(s2)  
fileP.close()  
fileQ.close()