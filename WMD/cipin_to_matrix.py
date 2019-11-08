# -*- encoding=utf-8 -*-

import numpy as np
from prettyprint import pp
import json
f = open("file_cipin_mapper.json").read()
cipins = json.loads(f)
f = open("vector_set.json").read()
vector_set = json.loads(f)
length = len(cipins)

def getMatrix(file):
    d_list = []
    cipin = cipins[file]
    word_list = cipin.keys()
    c_matrix = np.array(vector_set[word_list[0]], np.float32)
    d_list.append(cipin[word_list[0]])
    for word in word_list[1:]:
        nplist = vector_set[word]
        npa = np.array(nplist, np.float32)
        c_matrix = np.row_stack((c_matrix, npa))
        d_list.append(cipin[word])
    da = np.array(d_list, np.float32)
    return (c_matrix,da)
if __name__ == '__main__':
    getMatrix("1000226.xml")

