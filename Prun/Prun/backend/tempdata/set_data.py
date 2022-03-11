'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2021-11-02 14:37:33
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import numpy as np
import time
import re
def set_node(job,id,appendix):
    loglist = None
    logDir = "Prun/data/{}/__cache__/logList.txt".format(job)
    
    
    
    controlDir = "Prun/data/{}/control.txt".format(job)
    r = open(controlDir,'r')
    string = r.readline()
    newString = string.split("@")
    newString[0] = 'r'
    newString[5] = id
    newString[7] = appendix
    newString_ = "@".join(newString)
    # print(newString)
    # print(newString_)
    r.close()
    
    with open(logDir, "r") as f:
        loglist = f.readlines()
    lengthStart = len(loglist)
    with open(controlDir,"w") as f:
        f.write(newString_)

    #! 读文件，暂时注释
    while True:
        try:
            r = open(controlDir,'r')
            string = r.readline()
            newString = string.split("@")
            tag = newString[0]
            r.close()
            if tag == 'n':
                break
            else:
                time.sleep(0.5)
        except Exception:
            time.sleep(0.5)
    step = 0
    with open(logDir, "r") as f:
        loglist = f.readlines()
        step = re.search(r'(\d+)',loglist[lengthStart])
        step = step.groups()[0]
    
    with open(logDir, "r") as f:
        loglist = f.readlines()
    dir = loglist[lengthStart][:-1]
    dataPath = None
    with open(controlDir,"r") as f:
        controlData = f.readline().strip()
        li = controlData.split("@")
        dataPath = li[11]
    path = dataPath+ '/' + dir
    # path = "Prun/data/{}/__cache__/data/".format(job) + dir
    r = np.load(path)
    dataType = []
    
    for i in r.keys():
        if "{}.weight".format(id) == i:
            dataType = dataType + ["weight","weightGrad"]
        if "{}.bias".format(id) == i:
            dataType = dataType + ["bias","biasGrad"]
    # print(dataType)
    # lengthStart = lengthStart - 1  #!
    # step = 24 #!
    return {"index":lengthStart,"step":step,"type":dataType}

