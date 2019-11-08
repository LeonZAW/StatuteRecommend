#encoding=utf-8
from prettyprint import pp

def test_flft_halfpass(number,k,t,mode):
    import json
    f = open(str(number) + "/files.json").read()
    Files = json.loads(f)
    f2 = open(str(number) + "/file_flftStd_mapper.json").read()
    Flftss = json.loads(f2)
    f3 = open(str(number) + "/file_wmd_mix_sim_10k_mapper.json").read()
    sims = json.loads(f3)
    testRes = []
    length = len(Files)
    if mode == "valid":
        start = length/5*3
        end = length/5*4
    else:
        start = length/5*4
        end = length
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
            sorted_list = sorted(counter, key=lambda x: x[1], reverse=True)
            recommendFlfts.add(sorted_list[0])
        count = 0
        for ft in recommendFlfts:
            if ft in Flft:
                count += 1
        precise = count * 1.0 / len(recommendFlfts)
        recall = count * 1.0 / len(Flft)
        testRes.append([precise, recall, file])
    f = open(str(number) + "/P_R_" + mode + "_311_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def test_flft(number,k,mode):
    import json
    f = open(str(number) + "/files.json").read()
    Files = json.loads(f)
    f2 = open(str(number) + "/file_flftStd_mapper.json").read()
    Flftss = json.loads(f2)
    f3 = open(str(number) + "/file_wmd_mix_sim_10k_mapper.json").read()
    sims = json.loads(f3)
    testRes = []
    length = len(Files)
    if mode == "valid":
        start = length / 5 * 3
        end = length / 5 * 4
    else:
        start = length / 5 * 4
        end = length
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
            sorted_list = sorted(counter, key=lambda x: x[1], reverse=True)
            recommendFlfts.add(sorted_list[0])
        count = 0
        for ft in recommendFlfts:
            if ft in Flft:
                count += 1
        precise = count * 1.0 / len(recommendFlfts)
        recall = count * 1.0 / len(Flft)
        testRes.append([precise, recall, file])
    f = open(str(number) + "/P_R_" + mode + "_all_311_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def test_flft_freq(number,k,t,mode):
    import json
    f = open(str(number) + "/files.json").read()
    Files = json.loads(f)
    f2 = open(str(number) + "/file_flftStd_mapper.json").read()
    Flftss = json.loads(f2)
    f3 = open(str(number) + "/file_wmd_mix_sim_2k_mapper.json").read()
    sims = json.loads(f3)
    f4 = open(str(number) + "/flft_freq_mapper.json").read()
    mapper = json.loads(f4)
    testRes = []
    length = len(Files)
    if mode == "valid":
        start = length / 5 * 3
        end = length / 5 * 4
    else:
        start = length / 5 * 4
        end = length
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
            if counter[ft] >= (mapper[ft]-t)*k:
                recommendFlfts.add(ft)
        if len(recommendFlfts)==0:
            sorted_list = sorted(counter, key=lambda x: x[1], reverse=True)
            recommendFlfts.add(sorted_list[0])
        count = 0
        for ft in recommendFlfts:
            if ft in Flft:
                count += 1
        precise = count * 1.0 / len(recommendFlfts)
        recall = count * 1.0 / len(Flft)
        testRes.append([precise, recall, file])
    f = open(str(number) + "/P_R_" + mode + "_freq_311_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def test_flft_top10(number,k,mode):
    import json
    f = open(str(number) + "/files.json").read()
    Files = json.loads(f)
    f2 = open(str(number) + "/file_flftStd_mapper.json").read()
    Flftss = json.loads(f2)
    f3 = open(str(number) + "/flft_top10.json").read()
    top10 = json.loads(f3)
    testRes = []
    length = len(Files)
    if mode == "valid":
        start = length / 5 * 3
        end = length / 5 * 4
    else:
        start = length / 5 * 4
        end = length
    from collections import defaultdict

    for file in Files[start:end]:
        Flft = Flftss[file]
        recommendFlfts = [flft[0] for flft in top10[:k]]
        count = 0
        for ft in recommendFlfts:
            if ft in Flft:
                count += 1
        precise = count * 1.0 / len(recommendFlfts)
        recall = count * 1.0 / len(Flft)
        testRes.append([precise, recall, file])
    f = open(str(number) + "/P_R_" + mode + "_top10_311_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def test_flft_topK(number,K,mode,isSim):
    import json
    f = open(str(number) + "/files.json").read()
    Files = json.loads(f)
    f2 = open(str(number) + "/file_flftStd_mapper.json").read()
    Flftss = json.loads(f2)
    f3 = open(str(number) + "/file_wmd_mix_sim_10k_mapper.json").read()
    sims = json.loads(f3)
    testRes = []
    length = len(Files)
    if mode == "valid":
        start = length / 5 * 3
        end = length / 5 * 4
    else:
        start = length / 5 * 4
        end = length

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
                if isSim:
                    counter[ft] =  counter[ft] + 1.0/(sim+0.1)
                else:
                    counter[ft] =  counter[ft] + 1.0
        sorted_list = sorted(counter.items(),key = lambda x:x[1],reverse = True)

        for i in xrange(min(K,len(sorted_list))):
            recommendFlfts.add(sorted_list[i][0])
        # save_AJJBQK()
        count = 0
        for ft in recommendFlfts:
            if ft in Flft:
                count += 1
        precise = count * 1.0 / len(recommendFlfts)
        recall = count * 1.0 / len(Flft)
        testRes.append([precise, recall, file])
    if isSim:
        fileName = "_topKsim"
    else:
        fileName = "_topK"
    f = open(str(number) + "/P_R_" + mode + fileName +"_311_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))

def countRes(number,mode, filename):
    import json
    f = open(str(number) + "/P_R_"+ mode + filename + "_2k.json").read()
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
def getRes(number):
    k,k_best,k_min = 10,10,1
    t,t_best,t_max = 0.1,0.1,0.9
    F_max = 0
    while k >= k_min:
        while t <= t_max:
            test_flft_halfpass(number,k,t,mode="valid")
            P, R = countRes(number,"valid","_311")
            F = 2.0/(1.0/P + 1.0/R)
            if F >= F_max:
                k_best = k
                t_best = t
                F_max = F
            t += 0.1
        k -= 1
        t = 0.1
    print k_best,t_best,F_max
    test_flft_halfpass(number,k_best, t_best,mode="test")
    P, R = countRes(number,"test","_311")
    F = 2.0 / (1.0 / P + 1.0 / R)
    testRes = {"bestK":k_best,"bestThreadhold":t_best,"ValidationF":F_max,"P":P,"R":R,"F":F}
    import json
    f = open(str(number) + "/result_311_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))

def getTopKRes(number,isSim,isAll):
    k,k_best,k_min = 10,10,1
    F_max = 0
    while k >= k_min:
        ratio = "_311"
        if isSim:
            filename = "_topKsim"
            test_flft_topK(number,k, "valid", isSim)
        elif isAll:
            filename = "_all"
            test_flft(number,k, "valid")
        else:
            filename = "_topK"
            test_flft_topK(number,k, "valid", isSim)
        P, R = countRes(number,"valid", filename+ratio)
        F = 2.0/(1.0/P + 1.0/R)
        if F >= F_max:
            k_best = k
            F_max = F
        k -= 1
    print k_best,F_max
    if isAll:
        test_flft(number,k_best, "test")
    else:
        test_flft_topK(number,k_best, "test", isSim)
    P, R = countRes(number,"test", filename+ratio)
    F = 2.0 / (1.0 / P + 1.0 / R)
    testRes = {"bestK":k_best,"ValidationF":F_max,"P":P,"R":R,"F":F}
    import json
    f = open(str(number) + "/result"+filename+ratio+"_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def getTop10Res(number):
    k,k_best,k_min = 10,10,1
    F_max = 0
    while k >= k_min:
        ratio = "_311"
        test_flft_top10(number,k, "valid")
        P, R = countRes(number,"valid", "_top10"+ratio)
        F = 2.0/(1.0/P + 1.0/R)
        # print k,P,R,F
        if F >= F_max:
            k_best = k
            F_max = F
        k -= 1
    print k_best,F_max
    test_flft_top10(number,k_best, "test")
    P, R = countRes(number,"test", "_top10"+ratio)
    F = 2.0 / (1.0 / P + 1.0 / R)
    testRes = {"bestK":k_best,"ValidationF":F_max,"P":P,"R":R,"F":F}
    import json
    f = open(str(number) + "/result"+"_top10"+ratio+"_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def getFreqRes(number):
    k, k_best, k_min = 10, 10, 1
    t, t_best, t_max = 0.1, 0.1, 0.9
    F_max = 0
    while k >= k_min:
        while t <= t_max:
            test_flft_freq(number, k, t, mode="valid")
            P, R = countRes(number, "valid", "_freq_311")
            F = 2.0 / (1.0 / P + 1.0 / R)
            if F >= F_max:
                k_best = k
                t_best = t
                F_max = F
            t += 0.1
        k -= 1
        t = 0.1
    print k_best, t_best, F_max
    test_flft_freq(number, k_best, t_best, mode="test")
    P, R = countRes(number, "test", "_freq_311")
    F = 2.0 / (1.0 / P + 1.0 / R)
    testRes = {"bestK": k_best, "bestThreadhold": t_best, "ValidationF": F_max, "P": P, "R": R, "F": F}
    import json
    f = open(str(number) + "/result_freq_311_2k.json", "w")
    data = json.dumps(testRes, ensure_ascii=False)
    f.write(data.encode('utf-8'))
if __name__ == '__main__':
    number = 0
    # getRes(number)
    # getTopKRes(number,False,False)
    # getTopKRes(number,True,False)
    # getTopKRes(number,False,True)
    getTop10Res(number)