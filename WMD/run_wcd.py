# -*- encoding=utf-8 -*-
import numpy as np
import json
import cipin_to_matrix as cm
f = open("9015_file.json").read()
files = json.loads(f)
print "Load complete"
from wcd import getWCD
sims = []
wmsims = []
import time
from cv2 import cv
start = time.clock()
files1 = files[10000:]
files2 = files[:10000]
k = 10
Length = len(files1)
for c,file in enumerate(files1):
    c_matrix,d_list = cm.getMatrix(file)
    signature1 = (c_matrix,d_list)
    heap_list = []
    for file2 in files2:
        c_matrix2, d_list2 = cm.getMatrix(file2)
        signature2 = (c_matrix2, d_list2)
        wcd = float(getWCD(signature1,signature2))
        heap_list.append([file2,wcd])
    sorted_list = sorted(heap_list, key=lambda x: x[1], reverse=False)
    saved_list = sorted_list[:100]
    sims.append([saved_list, file])
    d_list = np.transpose(d_list)
    signature1 = np.column_stack((d_list, c_matrix))
    wmd_mix_sims = []
    for wcd_gram in saved_list[:2*k]:
        file2 = wcd_gram[0]
        wcd = wcd_gram[1]
        c_matrix2, d_list2 = cm.getMatrix(file2)
        d_list2 = np.transpose(d_list2)
        signature2 = np.column_stack((d_list2, c_matrix2))
        pp = cv.fromarray(signature1)
        qq = cv.fromarray(signature2)
        emd = cv.CalcEMD2(pp, qq, cv.CV_DIST_L2)
        wmd_mix_sims.append([file2, emd])
    sorted_list = sorted(wmd_mix_sims, key=lambda x: x[1], reverse=False)
    wmsims.append([sorted_list, file])
    if ((c + 1) % 50 == 0):
        print "进度:", (c * 1.0 + 1) / Length
end = time.clock()
print end-start
f2 = open("wcd_sim_10000.json", "w")
data = json.dumps(sims, ensure_ascii=False)
f2.write(data.encode('utf-8'))
f3 = open("wmd_mix_sim_10000_2k.json", "w")
data = json.dumps(wmsims, ensure_ascii=False)
f3.write(data.encode('utf-8'))