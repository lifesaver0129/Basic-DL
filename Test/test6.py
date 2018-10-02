
import pymysql, nltk

zaloraid = open("C:/Users/Administrator/Desktop/zalora_id.txt", encoding='utf8').readlines()
newzaloraid = open("C:/Users/Administrator/Desktop/new_zalora_id.txt", encoding='utf8').readlines()


zaloraidlist = []
for ele in zaloraid:
    ele = ele.strip('\n')
    zaloraidlist.append(ele)

db = pymysql.connect("localhost", "root", "123456", "clean_data_zalora", charset="utf8")
cursor = db.cursor()


newzaloraidlist = []
for ele in newzaloraid:
    ele = ele.strip('\n')
    newzaloraidlist.append(ele)

for ele in zaloraidlist:
    print(ele)
    if ele not in newzaloraidlist:
        sqlstring = 'DELETE FROM clean_data_zalora.product where idproduct = %s'
        cursor.execute(sqlstring, ele)
        db.commit()#需要这一句才能保存到数据库中

db.close()