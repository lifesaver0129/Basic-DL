#1
# asos_cate = open("C:/Users/Administrator/Desktop/asos id.txt", encoding='utf8').readlines()
# bad_id = open("C:/Users/Administrator/Desktop/badid.txt", encoding='utf8').readlines()
#
# bad_idlist = []
#
#
# for ele in bad_id:
#     ele = ele.strip('\n')
#     bad_idlist.append(ele)

#2
# asos_cate = open("C:/Users/Administrator/Desktop/newoutput.txt", encoding='utf8').readlines()
# matchlist = open("C:/Users/Administrator/Desktop/ASOS ID newID similarlist matchlist.txt", encoding='utf8').readlines()


#1
# for ele in asos_cate:
#     ele = ele.strip('\n')
#     elelist = ele.split('\t')
#     if elelist[0] not in bad_idlist:
#         print(elelist[0])
#         with open('C:/Users/Administrator/Desktop/newoutput.txt', 'a', encoding='utf8') as f:
#             f.write(str(elelist[0]) + '\t' + str(elelist[1]) + '\t' + str(elelist[2]) + '\n')

#2
# idlist = []
# newidlist = []
#
#
# for ele in matchlist:
#     ele = ele.strip('\n')
#     elelist = ele.split('\t')
#     idlist.append(elelist[0])
#     newidlist.append(elelist[1])
#
#
#
#
# for ele in asos_cate:
#     ele = ele.strip('\n')
#     print(ele)
#     elelist = ele.split('\t')
#     productId = elelist[0]
#     if productId in idlist:
#         index_num = idlist.index(productId)
#         newid = newidlist[index_num]
#         with open('C:/Users/Administrator/Desktop/00.txt', 'a', encoding='utf8') as f:
#             f.write(str(elelist[0]) + '\t' + str(newid) + '\t' + str(elelist[1]) + '\t' + str(elelist[2]) + '\n')



diclist = open("C:/Users/Administrator/Desktop/dic.txt", encoding='utf8').readlines()
matchlist = open("C:/Users/Administrator/Desktop/ASOS ID newID similarlist matchlist.txt", encoding='utf8').readlines()

oldidlist = []
newidlist = []
catelist = []

for ele in diclist:
    ele = ele.strip('\n')
    elelist = ele.split('\t')
    oldidlist.append(elelist[0])
    newidlist.append(elelist[1])
    catelist.append(elelist[2].strip(';'))



def findcate(oldidlist, newidlist, catelist, newid):
    result = ''
    number = 0
    if newid in newidlist:
        number = newidlist.index(newid)
        result = catelist[number]
    return result


for ele in matchlist:
    ele = ele.strip('\n')
    elelist = ele.split('\t')

    oldid = elelist[0]
    print(oldid)

    if oldid in oldidlist:

        newid = elelist[1]

        similarlist = elelist[2].split(';')

        matchlist = elelist[3].split(';')

        trans1 = findcate(oldidlist, newidlist, catelist, newid)

        trans2 = ''
        for ele in similarlist:
            ele = ele.strip()
            trans2 = trans2 + '||' + findcate(oldidlist, newidlist, catelist, ele)

        trans3 = ''
        for ele in matchlist:
            ele = ele.strip()
            trans3 = trans3 + '||' + findcate(oldidlist, newidlist, catelist, ele)



        with open('C:/Users/Administrator/Desktop/00000.txt', 'a', encoding='utf8') as f:
            f.write(str(oldid) + '\t' + str(trans1) + '\t' + str(trans2) + '\t' + str(trans3) + '\n')
