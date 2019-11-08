# -*- encoding=utf-8 -*-
totalFilesNumber = 3000
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim import corpora, models
import numpy as np
import json
from prettyprint import pp
f = open("WMD/jiaba.json").read()
jiebas = json.loads(f)
train = [item[0] for item in jiebas[:totalFilesNumber / 5 * 3]]
dictionary = Dictionary(train)
def train_model():
    corpus = [ dictionary.doc2bow(text) for text in train ]
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)
    #模型的保存/ 加载
    lda.save('lda.model')
lda = models.ldamodel.LdaModel.load('lda.model')
def get_vec(s):
    doc_bow = dictionary.doc2bow(s)
    doc_lda = lda[doc_bow]
    vec1 = [float(0.0)] * 20
    for i in doc_lda:
        idx = i[0]
        vec1[idx] = float(i[1])
    return vec1
def count_vec():
    sims = []
    for jieba_gram in jiebas:
        jieba = jieba_gram[0]
        file = jieba_gram[1]
        vec = get_vec(jieba)
        sims.append([vec, file])
    f = open("lda_vec.json", "w")
    data = json.dumps(sims, ensure_ascii=False)
    f.write(data.encode('utf-8'))
    print "vec complete"

def cos_dist(A,B):

    A = np.array(A)
    B = np.array(B)
    num = float(np.vdot(A,B))
    denom = float(np.linalg.norm(A) * np.linalg.norm(B))
    if denom == 0:
        cos = -1
    else:
        cos = num / denom
    return cos
def count_sim():
    import json
    f = open("lda_vec.json").read()
    vecs = json.loads(f)
    sims = []
    for c,vec_gram in enumerate(vecs[totalFilesNumber / 5 * 3:]):
        vec = vec_gram[0]
        file = vec_gram[1]
        slist = []
        for vec_gram2 in vecs[:totalFilesNumber / 5 * 3]:
            vec2 = vec_gram2[0]
            file2 = vec_gram2[1]
            cos = cos_dist(vec,vec2)
            slist.append([file2,cos])
        sorted_list = sorted(slist, key=lambda x: x[1], reverse=True)
        sims.append([sorted_list[:100], file])
        if ((c + 1) % 50 == 0):
            print "进度:", (c * 1.0 + 1) / 600
    f = open("lda_sim.json", "w")
    data = json.dumps(sims, ensure_ascii=False)
    f.write(data.encode('utf-8'))
    print "sim complete"
if __name__ == '__main__':
    # train_model()
    count_vec()
    count_sim()