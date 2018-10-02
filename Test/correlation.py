
import numpy as np
from scipy import spatial



def findIndices_Nmax(inputArray, n):
    inputArray = np.asarray(inputArray)
    return inputArray.argsort()[-n:][::-1]

def consineSim(listA, listB):
    return 1 - spatial.distance.cosine(listA, listB)


def findrecbyid(productID):
    result = ''
    sqlstring = 'select '



names = open("C:/Users/Administrator/Desktop/mid.txt", encoding='utf8').readlines()
recommendations = open("C:/Users/Administrator/Desktop/rec.txt", encoding='utf8').readlines()

namesList = []
recIDList = []
# recList = []
#1ID	2Email(user)	3Product ID test	4Wishlist ID	5Rec Type	6Product Group

for ele in names:
    ele = ele.strip('\n')
    namesList.append(ele)

for ele in recommendations:
    ele = ele.strip('\n')
    elelist = ele.split('\t')
    recIDList.append(elelist)



for ele in recIDList:
    stringlist = ''
    for eleele in ele:
        eleele = int(eleele)
        stringlist = stringlist + ';' + namesList[eleele]
    with open('C:/Users/Administrator/Desktop/output.txt', 'a', encoding='utf8') as f:
        f.write(stringlist + '\n')







        # sequence = []
    # score = 0
    # reclist = ele[0].split(';')
    # type = ele[1]
    # simlist = ele[2].split(';')
    # matlist = ele[3].split(';')
#
#     if type == 'Similar':
#         print(set(simlist).intersection(reclist))
#     if type == 'M&M':
#         print(set(matlist).intersection(reclist))


    # if type == 'Similar':
    #     for eachrec in reclist:
    #         if eachrec in simlist:
    #             sequence.append(simlist.index(eachrec))
    #         else:
    #             sequence.append('NULL')
    # if type == 'M&M':
    #     for eachrec in reclist:
    #         if eachrec in matlist:
    #             sequence.append(matlist.index(eachrec))
    #         else:
    #             sequence.append('NULL')

    # print(sequence)

# for ele in recommendations:
#     ele = ele.strip('\n')
#     elelist = ele.split('\t')
#     recIDList.append(elelist[0])
#     recList.append(elelist[1])
#
#
# for eachrow in midList:
#     productID = eachrow[0]
#     recstring = recList[recIDList.index(productID)]
#     with open('C:/Users/Administrator/Desktop/output.txt', 'a', encoding='utf8') as f:
#         f.write(str(eachrow) + '\t' + recstring + '\n')





# for eachrow in midList:
#     index = int(eachrow[0])
#     similarnum = 0
#     matchnum = 0
#
#     similarstring = ''
#     matchstring = ''
#
#     tag1 = bool(midList[index][5])
#     tag2 = bool(midList[index+1][5])
#
#     tag3 = bool(midList[index+2][5])
#     if midList[index+2][4] == 'Similar':
#         similarnum = similarnum + 1
#         similarstring = similarstring + ';' + str(midList[index+2][2])
#     if midList[index+2][4] == 'M&M':
#         matchnum = matchnum + 1
#         matchstring = matchstring + ';' + str(midList[index+2][2])
#
#     tag4 = bool(midList[index+3][5])
#     if midList[index+3][4] == 'Similar':
#         similarnum = similarnum + 1
#         similarstring = similarstring + ';' + str(midList[index+3][2])
#
#     if midList[index+3][4] == 'M&M':
#         matchnum = matchnum + 1
#         matchstring = matchstring + ';' + str(midList[index+3][2])
#
#     tag5 = bool(midList[index+4][5])
#     if midList[index+4][4] == 'Similar':
#         similarnum = similarnum + 1
#         similarstring = similarstring + ';' + str(midList[index+4][2])
#
#     if midList[index+4][4] == 'M&M':
#         matchnum = matchnum + 1
#         matchstring = matchstring + ';' + str(midList[index+4][2])
#
#     tag6 = bool(midList[index+5][5])
#     if midList[index+5][4] == 'Similar':
#         similarnum = similarnum + 1
#         similarstring = similarstring + ';' + str(midList[index+5][2])
#
#     if midList[index+5][4] == 'M&M':
#         matchnum = matchnum + 1
#         matchstring = matchstring + ';' + str(midList[index+5][2])
#
#     tag7 = bool(midList[index+6][5])
#     if midList[index+6][4] == 'Similar':
#         similarnum = similarnum + 1
#         similarstring = similarstring + ';' + str(midList[index+6][2])
#
#     if midList[index+6][4] == 'M&M':
#         matchnum = matchnum + 1
#         matchstring = matchstring + ';' + str(midList[index+6][2])
#
#     tag8 = bool(midList[index+7][5])
#     if midList[index+7][4] == 'Similar':
#         similarnum = similarnum + 1
#         similarstring = similarstring + ';' + str(midList[index+7][2])
#
#     if midList[index+7][4] == 'M&M':
#         matchnum = matchnum + 1
#         matchstring = matchstring + ';' + str(midList[index + 7][2])
#
#     tag9 = bool(midList[index+8][5])
#     if midList[index+8][4] == 'Similar':
#         similarnum = similarnum + 1
#         similarstring = similarstring + ';' + str(midList[index+8][2])
#
#     if midList[index+8][4] == 'M&M':
#         matchnum = matchnum + 1
#         matchstring = matchstring + ';' + str(midList[index + 8][2])
#
#     if similarnum == 3 and matchnum == 4 and (midList[index][4] != midList[index+1][4]) and midList[index][2] == midList[index+1][2] and tag1 == True and tag2 == True and tag3 == False and tag4 == False and tag5 == False and tag6 == False and tag7 == False and tag8 == False and tag9 == False:
#         if midList[index][5] == 'group1' and midList[index+1][5] == 'group1':
#             with open('C:/Users/Administrator/Desktop/output.txt', 'a', encoding='utf8') as f:
#                 f.write(str(midList[index][2]) + '\t' + similarstring + '\t' + 'Similar' + '\n')
#                 f.write(str(midList[index][2]) + '\t' + matchstring + '\t' + 'M&M' + '\n')
                # f.write(str(midList[index]) + '\n')
                # f.write(str(midList[index+1]) + '\n')
                # f.write(str(midList[index+2]) + '\n')
                # f.write(str(midList[index+3]) + '\n')
                # f.write(str(midList[index+4]) + '\n')
                # f.write(str(midList[index+5]) + '\n')
                # f.write(str(midList[index+6]) + '\n')
                # f.write(str(midList[index+7]) + '\n')
                # f.write(str(midList[index+8]) + '\n')
