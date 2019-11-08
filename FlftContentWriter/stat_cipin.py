# -*- encoding=utf-8 -*-
from prettyprint import pp
import math
def docs(w, D):
    c = 0
    for d in D:
        if w in d:
            c = c + 1;
    return c
def stat():
    D = []
    W = set()
    import json
    f = open("fls.json").read()
    fls = json.loads(f)
    # count = 0
    for fl in fls:
        import re
        fl = re.sub(u"\(.*?\)", u"", fl)
        D.append(fl)
        W = W | set(fl)
    # 计算idf
    idf_dict = {}
    n = len(fls)
    # idf = log(n / docs(w, D))
    for w in list(W):
        idf = math.log(n * 1.0 / docs(w, D))
        idf_dict[w] = idf
    # sorted_list = sorted(idf_dict.items(), key=lambda x: x[1])
    # pp(sorted_list[:100])
    f = open("idf_dict2.json", "w")
    data = json.dumps(idf_dict, ensure_ascii=False)
    f.write(data.encode('utf-8'))
def printf():
    import json
    f = open("fls_pin.json").read()
    list = json.loads(f)
    list2 = [item[0] for item in list[:30]]
    f = open("idf_top30.json", "w")
    data = json.dumps(list2, ensure_ascii=False)
    f.write(data.encode('utf-8'))
if __name__ == '__main__':
    stat()
    # printf()