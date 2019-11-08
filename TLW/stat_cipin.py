# -*- encoding=utf-8 -*-
from prettyprint import pp
totalFilesNumber = 3000
import numpy as np
import math
def docs(w, D):
    c = 0
    for d in D:
        if w in d:
            c = c + 1;
    return c
def stat_idf():
    D = []
    W = set()
    import json
    f = open("WMD/jiaba.json").read()
    jiebas = json.loads(f)[:totalFilesNumber/5*3]
    # count = 0
    for jieba_gram in jiebas:
        jieba = jieba_gram[0]
        D.append(jieba)
        W = W | set(jieba)
    # 计算idf

    idf_dict = {}
    n = len(jiebas)
    # idf = log(n / docs(w, D))
    import math
    for w in list(W):
        idf = math.log(n * 1.0 / docs(w, D))
        idf_dict[w] = idf
    f = open("TF-IDF/idf.json", "w")
    data = json.dumps(idf_dict, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def stat_tfidf():
    import json
    f = open("WMD/jiaba.json").read()
    jiebas = json.loads(f)[:totalFilesNumber / 5 * 3]
    f = open("TF-IDF/idf.json").read()
    idf_dict = json.loads(f)
    tf_idf = []
    print len(jiebas)
    for jieba_gram in jiebas:
        jieba = jieba_gram[0]
        file = jieba_gram[1]
        from collections import defaultdict
        cipin = defaultdict(float)

        count = 0
        for word in jieba:
            if word in idf_dict:
                cipin[word] = cipin[word] + 1
                count = count + 1
        for key in cipin.keys():
            cipin[key] = cipin[key] / count * idf_dict[key]
        sorted_list = sorted(cipin.items(), key=lambda x: x[1],reverse=True)
        for item in sorted_list[:3]:
            if item[0] not in tf_idf:
                tf_idf.append(item[0])

    print len(tf_idf)
    f = open("TF-IDF/tf_idf.json", "w")
    data = json.dumps(tf_idf, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def count_vec():
    import json
    f = open("WMD/jiaba.json").read()
    jiebas = json.loads(f)
    f = open("TF-IDF/tf_idf.json").read()
    tf_idf = json.loads(f)

    length = len(tf_idf)
    sims = []
    for jieba_gram in jiebas:
        vec = [0]*length
        jieba = jieba_gram[0]
        file = jieba_gram[1]

        for word in jieba:
            if word in tf_idf:
                idx = tf_idf.index(word)
                vec[idx] = vec[idx] + 1
        sims.append([vec, file])
    f = open("TF-IDF/tf_idf_vec.json", "w")
    data = json.dumps(sims, ensure_ascii=False)
    f.write(data.encode('utf-8'))
    print "vec complete"
def count_sim():
    import json
    f = open("TF-IDF/tf_idf_vec.json").read()
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
            print "进度:", (c * 1.0 + 1) / len(vecs)
    f = open("TF-IDF/tf_idf_sim.json", "w")
    data = json.dumps(sims, ensure_ascii=False)
    f.write(data.encode('utf-8'))
    print "sim complete"
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

if __name__ == '__main__':
    # stat_idf()
    # stat_tfidf()
    count_vec()
    count_sim()
