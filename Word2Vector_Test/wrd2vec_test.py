# -*- coding: utf-8 -*-

from gensim.models import Word2Vec
import gensim

model = gensim.models.KeyedVectors.load_word2vec_format('D:/lemmas.cbow.s100.w2v.bin', binary=True)
ans = model.most_similar('harjumaa')
print(ans)
