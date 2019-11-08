# encoding=utf-8
import re
from prettyprint import pp
import json
f = open("idf_dict.json").read()
idf_dict = json.loads(f)
def point(zi):
    if zi in idf_dict:
        return idf_dict[zi]
    return 1
def getStdFlft(flft):
    import json
    f = open("fls.json").read()
    list = json.loads(f)

    NAlist = [
        u"最高人民法院 最高人民检察院 公安部 司法部印发《关于对判处管制、宣告缓刑的犯罪分子适用禁止令有关问题的规定（试行）》的通知(2011)",
        u"最高人民法院研究室关于对保险法规定的“明确说明”应如何理解的问题的答复",
        u"陕西省高级人民法院关于审理道路交通事故损害赔偿案件若干问题的指导意见（试行）",
        u"山东省实施《中华人民共和国道路交通安全法》办法",
        u"陕西省实施《中华人民共和国道路交通安全法》办法",
        u"福建省实施《中华人民共和国道路交通安全法》办法",
        u"湖南省实施《中华人民共和国道路交通安全法》办法",
        u"浙江省实施《中华人民共和国道路交通安全法》办法",
        u"最高人民法院关于审理涉及机动车交通事故责任强制保险案件若干问题的意见",
        u"机动车驾驶员培训管理规定",
        u"甘肃省道路交通安全条例",
        u"黑龙江省道路交通安全条例",
        u"天津市道路交通安全管理若干规定",
        u"宁夏回族自治区道路交通安全条例",
        u"广东省高级人民法院关于审理刑事附带民事诉讼若干问题的指导意见",
        u"广东省道路交通安全条例",
        u"内蒙古自治区道路交通事故损害赔偿标准和计算方法",
        u"最高人民法院研究室关于对保险法第十七条规定的“明确说明”应如何理解的问题的答复(2000)",
        u"最高人民法院 最高人民检察院 公安部关于办理醉酒驾驶机动车刑事案件适用法律若干问题的意见(2013)",
        u"最高人民法院印发《关于贯彻宽严相济刑事政策的若干意见》的通知()",
        u"最高人民法院、最高人民检察院、司法部关于适用简易程序审理公诉案件的若干意见",
        u"最高人民法院、最高人民检察院、司法部关于适用普通程序审理“被告人认罪”案件的若干意见（试行）",
        u"最高人民法院关于审理刑事附带民事诉讼案件有关问题的批复(2000)",
        u"最高人民法院关于刑事附带民事诉讼范围问题的规定(2000)",
        u"上海市关于实施《中华人民共和国妇女权益保障法》办法",
        u"安徽省淮南市中级人民法院关于审理离婚纠纷案件若干问题的指导意见",
        u"最高人民法院关于适用《中华人民共和国刑事诉讼法》执行程序若干问题的解释(2013)",
        u"最高人民法院关于贯彻执行《中华人民共和国民法通则》若干问题的意见（试行）(1988)",
        u"最高人民法院关于调整高级人民法院和中级人民法院管辖第一审民商事案件标准的通知(2015)",
        u"最高人民法院关于人民法院审理未办结婚登记而以夫妻名义同居生活案件的若干意见(1989)",
        u"道路运输条例"
    ]
    list2 = []
    list.extend(NAlist)
    for fl in list:
        if fl not in list2:
            list2.append(fl)
    flft = re.sub(u"第.*?条", u"", flft)
    flft = re.sub(u"《", u"", flft)
    flft = re.sub(u"》", u"", flft)
    from collections import defaultdict
    counter = defaultdict(float)
    for flraw in list2:
        flraw = re.sub(u"\(.*?\)", u"", flraw)
        fl = re.sub(u"《", u"", flraw)
        fl = re.sub(u"》", u"", fl)
        # point = 1
        for zi in flft:
            if zi in fl:
                counter[flraw] = counter[flraw] + point(zi)
            else:
                counter[flraw] = counter[flraw] - point(zi)
        for zi in fl:
            if zi in flft:
                counter[flraw] = counter[flraw] + point(zi)
            else:
                counter[flraw] = counter[flraw] - point(zi)
    l = len(flft)
    sorted_list = sorted(counter.items(), key=lambda x: x[1]+l-len(x[0]), reverse=True)
    # pp(sorted_list)
    return sorted_list[0][0]
def solve():
    import json
    f2 = open("Flft_55000_2.json").read()
    Flftfiles2 = json.loads(f2)
    f11 = open("Flft_55000_11.json").read()
    Flftfiles11 = json.loads(f11)
    for count,flft_gram in enumerate(Flftfiles2[8000:8500]):
        flftGroup = flft_gram[0]
        flftGroup11 = Flftfiles11[count][0]
        if len(flftGroup)!=len(flftGroup11):
            continue
        for c,flft in enumerate(flftGroup):
            flft = re.sub(u"第.*?条$", u"", flft)
            flft11 = re.sub(u"第.*?条$", u"", flftGroup11[c])
            flft11 = re.sub(u"\(.*?\)$", u"", flft11)
            stdFlft = getStdFlft(flft)
            if flft11 != stdFlft:
                pp([flft,stdFlft,flft11])

if __name__ == '__main__':
    flft = u"《刑事诉讼法》"
    print getStdFlft(flft)
    # solve()