# encoding=utf-8
def getFile():
    import json
    f = open("Flft_2014.json").read()
    Flftfiles = json.loads(f)
    Flfts = []
    for count, flft_gram in enumerate(Flftfiles[0:3000]):
        # flftGroup = flft_gram[0]
        file = flft_gram[1]
        flftGroup2 = []
        # for flft in flftGroup:
                # re.sub(u"第.*?条$", u"", flft)
            # flftGroup2.append(flft)
            # all_flft[flftGroup[idx]] += 1
        Flfts.append(file)
        if ((count + 1) % 500 == 0):
            print "进度:", (count * 1.0 + 1) / 3000
    f = open("2014_file.json", "w")
    data = json.dumps(Flfts, ensure_ascii=False)
    f.write(data.encode('utf-8'))

# def getFlft():
#     import re
#     import json
#     f = open("Flft_2014.json").read()
#     Flftfiles = json.loads(f)
#     f = open("2014_file_3000.json").read()
#     files = json.loads(f)
#     Flfts = []
#     for count, flft_gram in enumerate(Flftfiles[0:3200]):
#         flftGroup = flft_gram[0]
#         file = flft_gram[1]
#         if file not in files:
#             continue
#         flftGroup2 = []
#         for flft in flftGroup:
#         # re.sub(u"第.*?条$", u"", flft)
#             ft = re.sub(u".*第", u"第", flft)
#             fl = getStdFlft(flft)
#             flftGroup2.append(fl+ft)
#         # all_flft[flftGroup[idx]] += 1
#         Flfts.append([flftGroup2,file])
#         if ((count + 1) % 500 == 0):
#             print "进度:", (count * 1.0 + 1) / 3000
#     f = open("2014_flft.json", "w")
#     data = json.dumps(Flfts, ensure_ascii=False)
#     f.write(data.encode('utf-8'))
#获取案件基本情况
def get_AJJBQK(filename):
    from xml.dom.minidom import parse
    DOMTree = parse(filename)
    writ = DOMTree.documentElement
    QW = writ.getElementsByTagName("QW")[0]
    AJJBQK =  QW.getElementsByTagName("AJJBQK")[0]
    case_text = AJJBQK.getAttribute("value")
    return case_text.strip()
def save_AJJBQK():
    file_dir = u"E:/毕业设计/素材/9015/"
    import json
    f = open("9015_file.json").read()
    Files = json.loads(f)
    AJJBQKs = []
    file_num = len(Files)
    for count, file in enumerate(Files):
        AJJBQK = get_AJJBQK(file_dir + file)
        AJJBQKs.append([AJJBQK,file])
        if ((count + 1) % 500 == 0):
            print "进度:", (count * 1.0 + 1) / file_num
    f = open("AJJBQK.json", "w")
    data = json.dumps(AJJBQKs, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def getFile3000():
    import json
    f = open("2014_file.json").read()
    Files = json.loads(f)[:3000]
    f = open("2014_file_3000.json", "w")
    data = json.dumps(Files, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def mapper(filename):
    import json
    f = open(filename+".json").read()
    json_data = json.loads(f)
    from collections import defaultdict
    mapper = defaultdict()

    for data in json_data:
        d = data[0]
        file = data[1]
        mapper[file] = d

    f = open("file_"+filename+"_mapper.json", "w")
    data = json.dumps(mapper, ensure_ascii=False)
    f.write(data.encode('utf-8'))
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

def AJJBQK2jieba():
    import json
    f = open("9015_file.json").read()
    Files = json.loads(f)
    f2 = open("file_AJJBQK_mapper.json").read()
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
    f = open("jiaba.json", "w")
    data = json.dumps(jiabas, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def jieba2W2V():
    import json
    f = open("jiaba.json").read()
    jiebas = json.loads(f)[:10000]
    train_data = [jieba[0] for jieba in jiebas]
    # pp(train_data)
    # 使用doc2vec模型训练法条，每个法条看做一篇文本
    import logging
    from gensim.models import Word2Vec
    logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)
    law_model = Word2Vec(train_data, size=100, workers=4,sg=1)
    law_model.save("word2vec_10000.model")
def writeFileVecMapper():
    import json
    f = open("cipin_vec_3000.json").read()
    Sims = json.loads(f)
    from collections import defaultdict
    mapper = defaultdict()

    for sim_gram in Sims:
        c_list = sim_gram[0]
        d_list = sim_gram[1]
        file = sim_gram[2]
        mapper[file] = [c_list,d_list]

    f = open("file_cipin_vec_3000_mapper.json", "w")
    data = json.dumps(mapper, ensure_ascii=False)
    f.write(data.encode('utf-8'))

def writeWcdSimMapper():
    import json
    f = open("wcd_sim_1800.json").read()
    Sims = json.loads(f)
    from collections import defaultdict
    mapper = defaultdict()

    for sim_gram in Sims:
        sims = sim_gram[0]
        file = sim_gram[1]
        mapper[file] = sims[:100]

    f = open("file_wcd_sim_1800_mapper_100.json", "w")
    data = json.dumps(mapper, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def getLength():
    import json
    f = open("9015_file.json").read()
    Sims = json.loads(f)
    print len(Sims)
if __name__ == '__main__':
    # mapper("Flft")
    # mapper("wmd_mix_sim_10000_2k")
    getLength()
    # save_AJJBQK()
    # AJJBQK2jieba()
    # jieba2W2V()