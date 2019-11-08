import numpy as np
import json
k = 10
f = open("9181_file.json")
Files = json.loads(f.read())
f2 = open("file_cipin_vec_12000_mapper.json")
cipins_mapper = json.loads(f2.read())
f3 = open("file_wcd_sim_7200_mapper_100.json")
wcd_sims_mapper = json.loads(f3.read())
f.close()
f2.close()
f3.close()
del(f)
del(f2)
del(f3)
import gc
gc.collect()
print "Load complete"
from cv2 import cv
sims = []
# import time
# start = time.clock()
from rwmd import *
from heap_sort import top_heap_sort
from insert_sort import *
count = 0
for file in Files[7200:]:
    count += 1
    cipin_gram = cipins_mapper[file]
    c_list = cipin_gram[0]
    d_list = cipin_gram[1]
    word_count = len(d_list)
    c_recover = np.array(c_list, np.float32).reshape(word_count, -1)
    d_recover = np.array(d_list, np.float32)
    signature1 = np.column_stack((np.transpose(d_recover), c_recover))

    wcd_sims = wcd_sims_mapper[file]
    wmd_mix_sims = [["Nil", 0]]
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
    top_heap_sort(wmd_mix_sims)
    wmd_mix_sims = wmd_mix_sims[1:]
    for wcd_sim_gram in wcd_sims[k:10*k]:
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
        InsertSortItem(wmd_mix_sims,[file_wcd, emd])
    sims.append([wmd_mix_sims,file])
    if count % 100 == 0:
        print count*1.0/4753,4753-count
# end = time.clock()
# print end-start
f = open("wmd_mix_sim_7200_10k.json", "w")
data = json.dumps(sims, ensure_ascii=False)
f.write(data.encode('utf-8'))