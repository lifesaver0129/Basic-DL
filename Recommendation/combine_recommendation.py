# -*- coding: utf-8 -*-



if __name__ == '__main__':
    leibie_1 = open("C:/Users/Administrator/Desktop/leibie_1.txt", encoding='utf8').readlines()
    leibie_2 = open("C:/Users/Administrator/Desktop/leibie_2.txt", encoding='utf8').readlines()
    
    leibie_1_ids = []
    leibie_2_ids = []
    
    for ele in leibie_1:
        ele = ele.strip('\n')
        ele_list = ele.split('\t')[0]
        leibie_1_ids.append(int(ele_list))
        
    for ele in leibie_2:
        ele = ele.strip('\n')
        ele_list = ele.split('\t')[0]
        leibie_2_ids.append(int(ele_list))
    intersection_list = list(set(leibie_1_ids)&set(leibie_2_ids))
    
    for eachid in intersection_list:
        rec_leibie1 = leibie_1[leibie_1_ids.index(eachid)].strip('\n').split('\t')[1].split(';')
        rec_leibie2 = leibie_2[leibie_2_ids.index(eachid)].strip('\n').split('\t')[1].split(';')
        result = list(set(rec_leibie1)&set(rec_leibie2))
        with open('C:/Users/Administrator/Desktop/finalresult.txt','a', encoding='utf8') as f:
            f.write(str(eachid) + '\t' + ';'.join(result) + '\n')
        
        