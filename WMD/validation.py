#encoding=utf-8
from prettyprint import pp
def test_flft_halfpass(k,t,mode):
    import json
    f = open("9015_file.json").read()
    Files = json.loads(f)
    f2 = open("file_Flft_mapper.json").read()
    Flftss = json.loads(f2)
    f3 = open("file_wmd_mix_sim_10000_2k_mapper.json").read()
    sims = json.loads(f3)
    testRes = []
    if mode == "valid":
        start = 10000
        end = 11000
    else:
        start = 11000
        end = 12845
    from collections import defaultdict

    for file in Files[start:end]:
        Flft = Flftss[file]
        counter = defaultdict(int)
        recommendFlfts = set()
        threadhold = k*t
        for file2_gram in sims[file][0:k]:
            file2 = file2_gram[0]
            Flfts = Flftss[file2]
            for ft in Flfts:
                counter[ft] = counter[ft] + 1
        for ft in counter.keys():
            if counter[ft]>=threadhold:
                recommendFlfts.add(ft)
        if len(recommendFlfts)==0:
            sorted_list = sorted(counter.items(), key=lambda x: x[1], reverse=True)
            recommendFlfts.add(sorted_list[0][0])
        count = 0
        for ft in recommendFlfts:
            if ft in Flft:
                count += 1
        precise = count * 1.0 / len(recommendFlfts)
        if len(Flft)==0:
            recall = 1
        else:
            recall = count * 1.0 / len(Flft)
        testRes.append([precise, recall, file])
    f = open("P_R_" + mode + "_1011_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def test_flft(k,mode):
    import json
    f = open("9015_file.json").read()
    Files = json.loads(f)
    f2 = open("file_Flft_mapper.json").read()
    Flftss = json.loads(f2)
    f3 = open("file_wmd_mix_sim_10000_2k_mapper.json").read()
    sims = json.loads(f3)
    testRes = []
    if mode == "valid":
        start = 10000
        end = 11000
    else:
        start = 11000
        end = 12845
    from collections import defaultdict

    for file in Files[start:end]:
        Flft = Flftss[file]
        counter = defaultdict(int)
        recommendFlfts = set()
        for file2_gram in sims[file][0:k]:
            file2 = file2_gram[0]
            Flfts = Flftss[file2]
            for ft in Flfts:
                counter[ft] = counter[ft] + 1
        for ft in counter.keys():
            recommendFlfts.add(ft)
        if len(recommendFlfts)==0:
            sorted_list = sorted(counter.items(), key=lambda x: x[1], reverse=True)
            recommendFlfts.add(sorted_list[0][0])
        count = 0
        for ft in recommendFlfts:
            if ft in Flft:
                count += 1
        precise = count * 1.0 / len(recommendFlfts)
        if len(Flft)==0:
            recall = 1
        else:
            recall = count * 1.0 / len(Flft)
        testRes.append([precise, recall, file])
    f = open("P_R_all_" + mode + "_1011_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def test_flft_topK(K,mode):
    import json
    f = open("9015_file.json").read()
    Files = json.loads(f)
    f2 = open("file_Flft_mapper.json").read()
    Flftss = json.loads(f2)
    f3 = open("file_wmd_mix_sim_10000_2k_mapper.json").read()
    sims = json.loads(f3)
    testRes = []
    if mode == "valid":
        start = 10000
        end = 11000
    else:
        start = 11000
        end = 12845

    from collections import defaultdict
    for file in Files[start:end]:
        Flft = Flftss[file]
        counter = defaultdict(float)
        recommendFlfts = set()
        for file2_gram in sims[file]:
            file2 = file2_gram[0]
            sim = file2_gram[1]
            Flfts = Flftss[file2]
            for ft in Flfts:
                # print sim
                # print file,file2
                counter[ft] =  counter[ft] + 1.0/(sim+1)
        sorted_list = sorted(counter.items(),key = lambda x:x[1],reverse = True)
        for i in xrange(min(K,len(sorted_list))):
            recommendFlfts.add(sorted_list[i][0])
        # save_AJJBQK()
        count = 0
        for ft in recommendFlfts:
            if ft in Flft:
                count += 1
        precise = count * 1.0 / len(recommendFlfts)
        if len(Flft)==0:
            recall = 1
        else:
            recall = count * 1.0 / len(Flft)
        testRes.append([precise, recall, file])
    f = open("P_R_" + mode + "_topKsim_1011_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))

def countRes(mode):
    import json
    f = open("P_R_"+ mode +"_topKsim_1011_2k.json").read()
    testRes = json.loads(f)
    count = 0
    precise_count = 0.0
    recall_count = 0.0
    for res in testRes:
        precise = res[0]
        recall = res[1]
        precise_count += precise
        recall_count += recall
        count += 1
    P = precise_count*1.0/count
    R = recall_count*1.0/count
    return (P,R)
def getRes():
    k,k_best,k_min = 10,10,1
    t,t_best,t_max = 0.1,0.1,0.7
    F_max = 0
    while k >= k_min:
        while t <= t_max:
            test_flft_halfpass(k,t,mode="valid")
            P, R = countRes(mode="valid")
            F = 2.0/(1.0/P + 1.0/R)
            if F >= F_max:
                k_best = k
                t_best = t
                F_max = F
            t += 0.1
        k -= 1
        t = 0.1
    print k_best,t_best,F_max
    test_flft_halfpass(k_best, t_best,mode="test")
    P, R = countRes(mode="test")
    F = 2.0 / (1.0 / P + 1.0 / R)
    testRes = {"bestK":k_best,"bestThreadhold":t_best,"ValidationF":F_max,"P":P,"R":R,"F":F}
    import json
    f = open("result_1011_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))

def getTopKRes():
    k,k_best,k_min = 10,10,1
    F_max = 0
    while k >= k_min:
        test_flft_topK(k,mode="valid")
        P, R = countRes(mode="valid")
        F = 2.0/(1.0/P + 1.0/R)
        if F >= F_max:
            k_best = k
            F_max = F
        k -= 1
    print k_best,F_max
    test_flft_topK(k_best,mode="test")
    P, R = countRes(mode="test")
    F = 2.0 / (1.0 / P + 1.0 / R)
    testRes = {"bestK":k_best,"ValidationF":F_max,"P":P,"R":R,"F":F}
    import json
    f = open("result_topKsim_1011_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))
if __name__ == '__main__':
    getTopKRes()