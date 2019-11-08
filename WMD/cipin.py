# -*- encoding=utf-8 -*-
import logging
from gensim.models.doc2vec import Doc2Vec
logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)
law_model = Doc2Vec.load("word2vec_10000.model")

import json
f = open("jiaba.json").read()
jiebas = json.loads(f)
sims = []
vector_set = {}
for c,jieba_gram in enumerate(jiebas):
    jieba = jieba_gram[0]
    file = jieba_gram[1]
    from collections import defaultdict
    cipin = defaultdict(float)

    count = 0
    for word in jieba:
        if word in law_model.wv.vocab:
            cipin[word] = cipin[word] + 1
            npa = law_model.wv[word]
            c_list = [vec.item() for vec in npa]
            vector_set[word] = c_list
            count = count + 1
    for key in cipin.keys():
        cipin[key] = cipin[key] / count
    sims.append([cipin, file])
    if ((c + 1) % 500 == 0):
        print "进度:", (c * 1.0 + 1) / 12000
f = open("cipin.json", "w")
data = json.dumps(sims, ensure_ascii=False)
f.write(data.encode('utf-8'))
f2 = open("vector_set.json", "w")
data = json.dumps(vector_set, ensure_ascii=False)
f2.write(data.encode('utf-8'))