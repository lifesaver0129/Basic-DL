# -*- coding: utf-8 -*-
import numpy as np
import pymysql
from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections
from nearpy.utils.utils import unitvec


def select_by_pk(pkey):
    #input primary key of a product;
    #output the vector of the product by np.array way.

    output = []
    sql_string = 'select vector from `b2c-src`.bucket_textile_color WHERE image_name = %s'

    cursor.execute(sql_string, pkey)
    result = cursor.fetchone()
    output = result[0].split(';')
    output = [float(i) for i in output]
    output = np.array(output)
    return output

def update_bucket(pk, bucket):
    #input primary key and the generated bucket of a product;
    #update the bucket in the database.

    sql_string = '''UPDATE `b2c-src`.bucket_textile_color SET
    bucket_code = %s
    WHERE
    image_name = %s'''

    cursor.execute(sql_string, (bucket, pk))
    db.commit()
    
    
# database connection

HOST = "158.132.122.212"
PORT = 13306
USER = "root"
PASSWORD = "tozmartdev2016"
DB = "b2c-src"
db = pymysql.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)
cursor = db.cursor()

# Dimension of our vector space
dimension = 288
# Create a random binary hash with 10 bits
rbp = RandomBinaryProjections('rbp', 12)

# Create engine with pipeline configuration
engine = Engine(dimension, lshashes=[rbp])

for each_image in open("C:/Users/Administrator/Desktop/pk.txt").readlines():
    each_image = each_image.strip('\n')
    each_vector = []
    each_vector = select_by_pk(each_image)
    engine.store_vector(each_vector, '%s' % each_image)
    
    each_bucket = ''.join(rbp.hash_vector(each_vector))

    update_bucket(each_image, each_bucket)
        
for each_image in open("C:/Users/Administrator/Desktop/pk.txt").readlines():
    each_image = each_image.strip('\n')
    each_vector = []
    each_vector = select_by_pk(each_image)
    
    # Get nearest neighbours
    N = engine.neighbours(each_vector)#     print(cosine_similarity(query, p_matrix[p_index.index(int(ele[1].strip('data_')))]))
    
    similarlist = []
    for ele in N:
        similarlist.append(str(ele[1]))

    with open('C:/Users/Administrator/Desktop/binarycode.txt', 'a', encoding='utf8') as f:
        f.write(each_image + '\t' + ';'.join(similarlist) + '\n')

