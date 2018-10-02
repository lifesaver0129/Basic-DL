'''
Created on 2016年12月22日

@author: Administrator
'''


import MyFunctions as MF

matrix = open("C:/Users/Administrator/Desktop/matrix.txt", encoding='utf8').readlines()


heitht = len(matrix)
width = len(matrix[0].split('\t'))

# print(heitht, width)

#each row
rowlist = []
for ele in matrix:
    ele = ele.strip('\n')
    eachrow = ele.split('\t')
    rowlist.append(eachrow)

iNumber = 2
while iNumber < len(rowlist):
    eachrow = rowlist[iNumber]
    jNumber = 2
    while jNumber < len(eachrow):
        if len(eachrow[jNumber]) > 0 and float(eachrow[jNumber]) > 0:
            with open('C:/Users/Administrator/Desktop/output.txt','a', encoding='utf8') as f:
                f.write(eachrow[0] + '\t' + eachrow[1] + '\t' + rowlist[0][jNumber] + '\t' + rowlist[1][jNumber] + '\t' + eachrow[jNumber] + '\n')
        jNumber = jNumber + 1
    iNumber = iNumber + 1










