# encoding=utf-8
from prettyprint import pp
import transfer
import validation

totalFilesNumber = 3000
def mapper(dir,filename):
    import json
    f = open(str(dir)+"/"+filename+".json").read()
    json_data = json.loads(f)
    from collections import defaultdict
    mapper = defaultdict()

    for data in json_data:
        d = data[0]
        file = data[1]
        mapper[file] = d

    f = open(str(dir)+"/file_"+filename+"_mapper.json", "w")
    data = json.dumps(mapper, ensure_ascii=False)
    f.write(data.encode('utf-8'))
    print "map "+filename+" complete"
#获取案件基本情况
def get_AJJBQK(filename):
    from xml.dom.minidom import parse
    DOMTree = parse(filename)
    writ = DOMTree.documentElement
    QW = writ.getElementsByTagName("QW")[0]
    AJJBQK =  QW.getElementsByTagName("AJJBQK")[0]
    case_text = AJJBQK.getAttribute("value")
    return case_text.strip()
def is_valid(filename):
    from xml.dom.minidom import parse
    DOMTree = parse(filename)
    writ = DOMTree.documentElement
    QW = writ.getElementsByTagName("QW")[0]
    if(len(QW.getElementsByTagName("AJJBQK"))==0):
        return False
    CPFXGCL = QW.getElementsByTagName("CPFXGC")
    if (len(CPFXGCL) == 0):
        return False
    CPFXGC = QW.getElementsByTagName("CPFXGC")[0]
    CUS_FLFT_FZ_RY = CPFXGC.getElementsByTagName("CUS_FLFT_FZ_RY")
    return len(CUS_FLFT_FZ_RY) != 0

def getFiles(dir):
    file_dir = u"E:/毕业设计/素材/9015/"
    import json
    import os
    validFiles = []
    cc = 0
    for _, _, files in os.walk(file_dir):
        file_num = len(files)
        for count, file in enumerate(files):
            if is_valid(file_dir + file):
                validFiles.append(file)
                cc += 1
            if ((count + 1) % 500 == 0):
                print "进度:", (count * 1.0 + 1) / file_num
    f = open(str(dir)+"/files.json", "w")
    global totalFilesNumber
    totalFilesNumber = len(validFiles)
    print "文书个数",totalFilesNumber
    data = json.dumps(validFiles, ensure_ascii=False)
    f.write(data.encode('utf-8'))
    print "files complete"
def save_AJJBQK(dir):
    file_dir = u"E:/毕业设计/素材/9015/"
    import json
    f = open(str(dir)+"/files.json").read()
    Files = json.loads(f)
    AJJBQKs = []
    file_num = len(Files)
    for count, file in enumerate(Files):
        AJJBQK = get_AJJBQK(file_dir + file)
        AJJBQKs.append([AJJBQK,file])
        if ((count + 1) % 500 == 0):
            print "进度:", (count * 1.0 + 1) / file_num
    f = open(str(dir)+"/AJJBQK.json", "w")
    data = json.dumps(AJJBQKs, ensure_ascii=False)
    f.write(data.encode('utf-8'))
    print "AJJBQK complete"
import re
import jieba
def deleteNyr(text):
    re_str = re.compile(u'\d+年|\d+月|\d+日|××××年|××月|××日|×')
    text = re_str.sub("", text)
    return text
def deleteNum(text):
    re_str = re.compile(u'\d|XX|&|rdquo|&rdquo|／|．|％|KVA|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z')
    text = re_str.sub("", text)
    return text
stopList = open("stopwords.dat").read().decode('utf-8').split('\n')
def getCutResult(text):
    # 使用jieba进行分词处理
    text = deleteNyr(text)
    text = deleteNum(text)
    text_l = jieba.lcut(text)

    law_clean = [text for text in text_l if text not in stopList]
    import re
    clean_text = re.sub(u"( ){2,}",u" "," ".join(law_clean))
    return clean_text.split()

def AJJBQK2jieba(dir):
    import json
    f = open(str(dir)+"/files.json").read()
    Files = json.loads(f)
    f2 = open(str(dir)+"/file_AJJBQK_mapper.json").read()
    mapper = json.loads(f2)
    jiabas = []
    file_num = len(Files)
    for count, file in enumerate(Files):
        AJJBQK = mapper[file]
        jieba = getCutResult(AJJBQK)

        jiabas.append([jieba,file])
        # text_list.append(text)
        if ((count + 1) % 500 == 0):
            print "进度:", (count * 1.0 + 1) / file_num

    # pp(jiabas)
    import json
    f = open(str(dir)+"/jiaba.json", "w")
    data = json.dumps(jiabas, ensure_ascii=False)
    f.write(data.encode('utf-8'))
    print "AJJBQK to jieba complete"
import logging
from gensim.models import Word2Vec
def jieba2W2V(dir):
    import json
    f = open(str(dir)+"/jiaba.json").read()
    jiebas = json.loads(f)[:totalFilesNumber/5*3]
    train_data = [jieba[0] for jieba in jiebas]
    # pp(train_data)
    # 使用doc2vec模型训练法条，每个法条看做一篇文本
    logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)
    law_model = Word2Vec(train_data, size=100, workers=4,sg=1)
    law_model.save(str(dir)+"/word2vec.model")
    print "word to vector complete"
def cipin(dir):

    logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)
    law_model = Word2Vec.load(str(dir)+"/word2vec.model")

    import json
    f = open(str(dir)+"/jiaba.json").read()
    jiebas = json.loads(f)
    sims = []
    for jieba_gram in jiebas:
        jieba = jieba_gram[0]
        file = jieba_gram[1]
        from collections import defaultdict
        cipin = defaultdict(float)

        count = 0
        for word in jieba:
            if word in law_model.wv.vocab:
                cipin[word] = cipin[word] + 1
                count = count + 1
        for key in cipin.keys():
            cipin[key] = cipin[key] / count
        sims.append([cipin, file])
    f = open(str(dir)+"/cipin.json", "w")
    data = json.dumps(sims, ensure_ascii=False)
    f.write(data.encode('utf-8'))
    print "cipin complete"
def c2m(dir):

    logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)
    law_model = Word2Vec.load(str(dir)+"/word2vec.model")
    import numpy as np
    from prettyprint import pp
    import json
    f = open(str(dir)+"/cipin.json").read()
    cipins = json.loads(f)
    features = []
    for cipin_gram in cipins:
        d_list = []
        cipin = cipin_gram[0]
        file = cipin_gram[1]
        keys = cipin.keys()
        c_matrix = law_model.wv[keys[0]]
        d_list.append(cipin[keys[0]])
        for key in keys[1:]:
            npa = law_model.wv[key]
            c_matrix = np.concatenate((c_matrix, npa), axis=0)
            d_list.append(cipin[key])
        # word_count = len(d_list)
        c_list = list(c_matrix)
        c_list = [vec.item() for vec in c_list]
        feature = [[c_list, d_list], file]
        # c_recover = np.array(c_list).reshape(word_count,-1)
        features.append(feature)
    f = open(str(dir)+"/cipin_vec.json", "w")
    data = json.dumps(features, ensure_ascii=False)
    f.write(data.encode('utf-8'))
    print "cipin to matrix complete"
def run_wcd(dir):
    import numpy as np
    import json
    f = open(str(dir)+"/files.json")
    Files = json.loads(f.read())
    f = open(str(dir)+"/file_cipin_vec_mapper.json")
    cipins_mapper = json.loads(f.read())
    f.close()
    print "Load complete"
    from wcd import getWCD
    sims = []
    import time
    start = time.clock()
    for file in Files[totalFilesNumber/5*3:]:
        cipin_gram = cipins_mapper[file]
        c_list = cipin_gram[0]
        d_list = cipin_gram[1]
        word_count = len(d_list)
        c_recover = np.array(c_list, np.float32).reshape(word_count, -1)
        d_revocer = np.array(d_list, np.float32)
        signature1 = (d_revocer, c_recover)
        from collections import deque
        heap_list = []
        for file2 in Files[:totalFilesNumber/5*3]:
            cipin_gram2 = cipins_mapper[file2]
            c_list2 = cipin_gram2[0]
            d_list2 = cipin_gram2[1]
            word_count2 = len(d_list2)
            c_recover2 = np.array(c_list2, np.float32).reshape(word_count2, -1)
            d_recover2 = np.array(d_list2, np.float32)
            signature2 = (d_recover2, c_recover2)
            wcd = float(getWCD(signature1, signature2))
            heap_list.append([file2, wcd])
        sorted_list = sorted(heap_list, key=lambda x: x[1], reverse=False)
        sims.append([sorted_list[:100], file])
    end = time.clock()
    print end - start
    f2 = open(str(dir)+"/wcd_sim.json", "w")
    data = json.dumps(sims, ensure_ascii=False)
    f2.write(data.encode('utf-8'))
def run_wmd_mix(dir):
    import numpy as np
    import json
    k = 10
    f = open(str(dir)+"/files.json")
    Files = json.loads(f.read())
    f2 = open(str(dir)+"/file_cipin_vec_mapper.json")
    cipins_mapper = json.loads(f2.read())
    f3 = open(str(dir)+"/file_wcd_sim_mapper.json")
    wcd_sims_mapper = json.loads(f3.read())
    f.close()
    f2.close()
    f3.close()
    del (f)
    del (f2)
    del (f3)
    import gc
    gc.collect()
    print "Load complete"
    from cv2 import cv
    sims = []
    # import time
    # start = time.clock()
    from insert_sort import InsertSortItem
    count = 0
    for file in Files[1800:]:
        count += 1
        cipin_gram = cipins_mapper[file]
        c_list = cipin_gram[0]
        d_list = cipin_gram[1]
        word_count = len(d_list)
        c_recover = np.array(c_list, np.float32).reshape(word_count, -1)
        d_recover = np.array(d_list, np.float32)
        signature1 = np.column_stack((np.transpose(d_recover), c_recover))

        wcd_sims = wcd_sims_mapper[file]
        wmd_mix_sims = []
        for wcd_sim_gram in wcd_sims[:k]:
            file_wcd = wcd_sim_gram[0]
            cipin_gram_wcd = cipins_mapper[file_wcd]
            c_list_wcd = cipin_gram_wcd[0]
            d_list_wcd = cipin_gram_wcd[1]
            word_count_wcd = len(d_list_wcd)
            c_recover_wcd = np.array(c_list_wcd, np.float32).reshape(word_count_wcd, -1)
            d_recover_wcd = np.array(d_list_wcd, np.float32)
            signature2 = np.column_stack((np.transpose(d_recover_wcd), c_recover_wcd))
            pp = cv.fromarray(signature1)
            qq = cv.fromarray(signature2)
            emd = cv.CalcEMD2(pp, qq, cv.CV_DIST_L2)
            wmd_mix_sims.append([file_wcd, emd])
        wmd_mix_sims = sorted(wmd_mix_sims, key=lambda x: x[1], reverse=False)
        for wcd_sim_gram in wcd_sims[k:10 * k]:
            file_wcd = wcd_sim_gram[0]
            cipin_gram_wcd = cipins_mapper[file_wcd]
            c_list_wcd = cipin_gram_wcd[0]
            d_list_wcd = cipin_gram_wcd[1]
            word_count_wcd = len(d_list_wcd)
            c_recover_wcd = np.array(c_list_wcd, np.float32).reshape(word_count_wcd, -1)
            d_recover_wcd = np.array(d_list_wcd, np.float32)
            # rwmd = getRWMD((c_recover,d_recover),(c_recover_wcd,d_recover_wcd))
            # if InsertTest(wmd_mix_sims, rwmd):
            signature2 = np.column_stack((np.transpose(d_recover_wcd), c_recover_wcd))

            pp = cv.fromarray(signature1)
            qq = cv.fromarray(signature2)
            emd = cv.CalcEMD2(pp, qq, cv.CV_DIST_L2)
            InsertSortItem(wmd_mix_sims, [file_wcd, emd])
        sims.append([wmd_mix_sims, file])
        if count % 100 == 0:
            print count * 1.0 / totalFilesNumber/5*2, totalFilesNumber/5*2 - count
    # end = time.clock()
    # print end-start
    f = open(str(dir)+"/wmd_mix_sim_10k.json", "w")
    data = json.dumps(sims, ensure_ascii=False)
    f.write(data.encode('utf-8'))

def getFromJson4(dir):
    import json
    f = open(str(dir) + "/flftDC.json").read()
    Flftfiles = json.loads(f)
    from collections import defaultdict
    all_flft = defaultdict(int)
    Flfts = []
    for count,flft_gram in enumerate(Flftfiles):
        flftGroup = flft_gram[0]
        file = flft_gram[1]
        flftGroup2 = []
        for flft in flftGroup:
            ft = re.sub(u"^.*?第", u"第", flft)
            flft = transfer.getStdFlft(flft)
            all_flft[flft+ft] += 1
            flftGroup2.append(flft+ft)
        Flfts.append([flftGroup2, file])

        if ((count + 1) % 500 == 0):
            print "进度:", (count * 1.0 + 1) / len(Flftfiles)
    pp(all_flft)
    f = open(str(dir) + "/flftStd.json", "w")
    data = json.dumps(Flfts, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def getTopFlft(dir,start,end):
    import json
    f = open(str(dir) + "/flftStd.json").read()
    Flftfiles = json.loads(f)
    length= len(Flftfiles)
    from collections import defaultdict
    all_flft = defaultdict(int)
    for count,flft_gram in enumerate(Flftfiles[length/5*start:length/5*end]):
        flftGroup = flft_gram[0]
        for flft in flftGroup:
            all_flft[flft] += 1

        if ((count + 1) % 500 == 0):
            print "进度:", (count * 1.0 + 1) / len(Flftfiles)
    sorted_list = sorted(all_flft.items(), key=lambda x: x[1], reverse=True)
    print sorted_list[0][1]
    sorted_list2 = []
    ll = length/5*end - length/5*start
    print ll
    for gram in sorted_list:
        sorted_list2.append([gram[0], gram[1] * 1.0 / ll])
    f = open(str(dir) + "/flft_freq_"+str(start)+str(end)+".json", "w")
    data = json.dumps(sorted_list2, ensure_ascii=False)
    f.write(data.encode('utf-8'))

def process(dir):
    getFiles(dir)
    save_AJJBQK(dir)
    mapper(dir,"AJJBQK")
    AJJBQK2jieba(dir)
    jieba2W2V(dir)
    cipin(dir)
    c2m(dir)
    mapper(dir,"cipin_vec")
    run_wcd(dir)
    mapper(dir, "wcd_sim")
    run_wmd_mix(dir)
    mapper(dir,"wmd_mix_sim_2k")

def transfer_flft(dir):
    getFromJson4(dir)
    mapper(dir,"flftStd")

def validate(dir):
    validation.getRes(dir)
    validation.getTopKRes(dir, False, False)
    validation.getTopKRes(dir, True, False)
    validation.getTopKRes(dir, False, True)

def print_stat_result(dir):
    print "案由："
    import json
    f = open(str(dir) + "/result_311_2k.json").read()
    # print "half_pass\t",json.loads(f)["F"]
    print json.loads(f)["F"]
    f = open(str(dir) + "/result_all_311_2k.json").read()
    # print "all_pass\t",json.loads(f)["F"]
    print json.loads(f)["F"]
    f = open(str(dir) + "/result_top10_311_2k.json").read()
    # print "top10_test\t",json.loads(f)["F"]
    print json.loads(f)["F"]
    f = open(str(dir) + "/result_topK_311_2k.json").read()
    # print "top_K\t\t",json.loads(f)["F"]
    print json.loads(f)["F"]
    f = open(str(dir) + "/result_topKsim_311_2k.json").read()
    # print "top_K_sim\t",json.loads(f)["F"]
    print json.loads(f)["F"]
    f = open(str(dir) + "/result_freq_311_2k.json").read()
    # print "flft_freq\t", json.loads(f)["F"]
    print json.loads(f)["F"]
def mapper_flft_freq(dir):
    import json
    f = open(str(dir) + "/flft_freq_03.json").read()
    Flftfreqs = json.loads(f)
    from collections import defaultdict
    mapper = defaultdict()

    for Flftfreq in Flftfreqs:
        Flft = Flftfreq[0]
        freq = Flftfreq[1]
        mapper[Flft] = freq

    f = open(str(dir) + "/flft_freq_mapper.json", "w")
    data = json.dumps(mapper, ensure_ascii=False)
    f.write(data.encode('utf-8'))
    print "map complete"
def print_top10_freq(dir):
    print "案由："
    import json
    f = open(str(dir) + "/flft_freq_03.json").read()
    freq03 = json.loads(f)[:10]
    f = open(str(dir) + "/flft_freq_34.json").read()
    freq34 = json.loads(f)[:10]
    f = open(str(dir) + "/flft_freq_45.json").read()
    freq45 = json.loads(f)[:10]
    for i in xrange(0,10):
        print freq03[i][0],freq03[i][1],freq34[i][0],freq34[i][1],freq45[i][0],freq45[i][1]

def left10(dir,filename):
    import json
    f = open(str(dir) + "/" + filename + ".json").read()
    json_data = json.loads(f)
    from collections import defaultdict
    mapper = defaultdict()

    for data in json_data:
        d = data[0]
        file = data[1]
        mapper[file] = d[:10]

    f = open(str(dir) + "/file_" + filename + "_mapper.json", "w")
    data = json.dumps(mapper, ensure_ascii=False)
    f.write(data.encode('utf-8'))
    print "map " + filename + " complete"
if __name__ == '__main__':
    run_wmd_mix("WMD_10k")
    mapper("WMD_10k", "wmd_mix_sim_10k")
    validate("WMD_10k")



    # left10("WMD_4k", "tf_idf_sim")
    # validate("TF-IDF")


    # import json
    #
    # f = open(str(10) + "/files.json").read()
    # Flftfreqs = json.loads(f)
    # print 978.0/len(Flftfreqs)
    # for i in xrange(0,11):
    #     getTopFlft(i,0,3)
        # getTopFlft(i,3,4)
        # getTopFlft(i,4,5)
        # mapper_flft_freq(i)
        # print_stat_result(i)

