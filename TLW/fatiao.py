#encoding=utf-8
import re
from xml.dom.minidom import parse
import json
from prettyprint import pp
num = [u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九']
k = [u'零', u'十', u'百', u'千', u'万', u'十', u'百']

# 取整取余并连接，返回连接好的字符串和余数
def turn(x, y):
    if y >= 1:
        a = x // pow(10, y)
        b = x % pow(10, y)
        c = num[a] + k[y]
        if y > 4 and b < pow(10, 4):
            c += k[4]
        if (len(str(x)) - len(str(b))) >= 2 and b != 0:
            c += k[0]
    else:
        a = x
        b = 0
        c = num[a]

    return (c, b,)

# 调用上一个函数，以保证进行完所有的数并返回
def tstr(x):
    if x==10:
        return k[1]
    if len(str(x))==2 and x/10==1:
        return k[1]+num[x%10]
    c = turn(x, (len(str(x)) - 1))
    a = c[0]
    b = c[1]
    while b != 0:
        a += turn(b, (len(str(b)) - 1))[0]
        b = turn(b, (len(str(b)) - 1))[1]
    return a

def getFlft(filename):
    DOMTree = parse(filename)
    writ = DOMTree.documentElement
    QW = writ.getElementsByTagName("QW")[0]
    CPFXGC = QW.getElementsByTagName("CPFXGC")[0]
    CUS_FLFT_FZ_RY = CPFXGC.getElementsByTagName("CUS_FLFT_FZ_RY")[0]
    CUS_FLFT_RYs = CUS_FLFT_FZ_RY.getElementsByTagName("CUS_FLFT_RY")
    return [CUS_FLFT_RY.getAttribute("value") for CUS_FLFT_RY in CUS_FLFT_RYs]
def normalize_flft(flft):
    #处理数字
    match = re.search(u"(\d{1,})", flft)
    while match:
        i = int(match.group())
        chm_num = tstr(i)

        flft = re.sub(u"(\d{1,})",chm_num,flft,count=1)
        match = re.search(u"(\d{1,})", flft)

    flft = re.sub(u"条.*?项", u"条", flft)
    flft = re.sub(u"条.*?款", u"条", flft)
    flft = re.sub(u"条第.*?", u"条", flft)
    flft = re.sub(u"﹤", u"〈", flft)
    flft = re.sub(u"﹥", u"〉", flft)
    return flft

def writeFlft(number):
    from collections import defaultdict
    all_flft = defaultdict(int)
    file_dir = u"E:/毕业设计/素材/9015/"
    f = open(str(number) + "/files.json").read()
    Files = json.loads(f)
    file_num = len(Files)
    Flfts = []
    for count, file in enumerate(Files):
        flftGroup = getFlft(file_dir + file)
        for idx,flft in enumerate(flftGroup):
            flftGroup[idx] = flft
            flftGroup[idx] = normalize_flft(flftGroup[idx])
            all_flft[re.sub(u"第.*?条",u"",flftGroup[idx])] += 1
            # all_flft[flftGroup[idx]] += 1
        Flfts.append([flftGroup,file])
        if ((count + 1) % 500 == 0):
            print "进度:", (count * 1.0 + 1) / file_num
    pp(all_flft)
    f = open(str(number) + "/flft.json", "w")
    data = json.dumps(Flfts, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def remove(flft):
    flft = re.sub(u"^.*?第",u"第",flft)
    if not u"第" in flft:
        return True
    if not u"条" in flft:
        return True
    return False
def getFromJson(number):
    import json
    f = open(str(number) + "/flft.json").read()
    Flftfiles = json.loads(f)
    from collections import defaultdict
    all_flft = defaultdict(int)
    Flfts = []
    for count,flft_gram in enumerate(Flftfiles):
        flftGroup = flft_gram[0]
        file = flft_gram[1]
        flftGroup2 = []
        for flft in flftGroup:
            if remove(flft):
                continue
            flft = re.sub(u"第二百二五十三条", u"第二百五十三条", flft)
            flft = re.sub(u"第三十二条（五）", u"第三十二条", flft)
            flft = re.sub(u"第一审民商事案件标准的通知》第三条", u"第三条", flft)

            all_flft[re.sub(u"^.*?第", u"第", flft)] += 1
            flftGroup2.append(flft)
            # all_flft[re.sub(u"第.*?条",u"",flftGroup[idx])] += 1
            # all_flft[flftGroup[idx]] += 1
        Flfts.append([flftGroup2, file])
        if ((count + 1) % 500 == 0):
            print "进度:", (count * 1.0 + 1) / 11953
    pp(all_flft)
    f = open(str(number) + "/flftDC.json", "w")
    data = json.dumps(Flfts, ensure_ascii=False)
    f.write(data.encode('utf-8'))

if __name__ == '__main__':
    # writeFlft("WMD")
    getFromJson("WMD")
