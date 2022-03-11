

import os
import shutil
import numpy as np
import sys
def searchDataPath(type,job,nodeId,npzPath):

    dic = {"weight_grad":"weightGrad","weight":"weight","bias":"bias","bias_grad":"biasGrad"}
    # nodeLog = "D:/prun/Prun/Prun/data/{}/__cache__/nodeLog".format(job)
    nodeLog = getPath("Prun/data/{}/__cache__/nodeLog".format(job))
    dataPath = ""
    with open("Prun/data/{}/control.txt".format(job),"r") as f:
        dataPath = f.readline().strip()
        cSegs = dataPath.split("@")
        dataPath = cSegs[11]
    seg = dataPath.split("/")
    header = seg[0]
    tag = False
    fileList = []
    for i in seg[1:]:
        if tag:
            header = header + "/" + i
            li = os.listdir(header)
            li_ = [f for f in li if f.isdigit()]
            li_ = sorted(li_,key=lambda x:int(x))
            for j in li_:
                path = header + "/" + j
                files = os.listdir(path)
                file_ = [f for f in files if "result_" in f]
                file_ = sorted(file_,key=lambda x:int(x[7:-4]))
                file_ = [path+"/"+f for f in file_]
                fileList.extend(file_)
                
        else:
            if "model" in i:
                tag = True
                header = header + "/" + i
                li = os.listdir(header)
                li_ = [f for f in li if f.isdigit()]
                li_ = sorted(li_,key=lambda x:int(x))
                for j in li_:
                    path = header + "/" + j
                    files = os.listdir(path)
                    file_ = [f for f in files if "result_" in f]
                    file_ = sorted(file_,key=lambda x:int(x[7:-4]))
                    file_ = [path+"/"+f for f in file_]
                    fileList.extend(file_)
            else:
                header = header + "/" + i
    records = []
    with open("{}/{}.text".format(nodeLog,nodeId),"r") as f:
        records = f.readlines()
        records = [record.strip() for record in records]
    def rule(name):
        seg = name.split("/")
        if seg[-1][7:-4] in records:
            return name
    fileList = list(filter(rule,fileList))
    r = []
    if npzPath:
        r = np.load(npzPath)
    else:
        r = np.load(fileList[0])
    shape = r["{}.{}".format(nodeId,type)].shape
    v = r["{}.{}".format(nodeId,type)]
    if "bias" in type:
        v = v.reshape(-1,1) 
    v = v.tolist()
    step = r["step"].tolist()
    pos = splitP(v)
    return {dic[type]:v,"tag":"success","op":tag,"shape":shape,"npzList":fileList,"step":step,"split":pos}

# list碾平
def flat(array):
    res = []
    for i in array:
        if isinstance(i, list):
            res.extend(flat(i))
        else:
            res.append(i)
    return res
# 统计四分位
def splitP(array):
    v = flat(array)
    v.sort()
    return [v[0],v[int(len(v)/4)],v[int(len(v)/2)],v[int(len(v)/4*3)],v[-1]]

def getPath(argv):
    basePath = sys.path[0]
    path = os.path.join(basePath,argv)
    return path

# def read

# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    # if kb >= 1024:
    #     M = kb / 1024
    #     if M >= 1024:
    #         G = M / 1024
    #         return "%fG" % (G)
    #     else:
    #         return "%.2fM" % (M)
    # else:
    #     return "%.2fkb" % (kb)
    
    M = kb / 1024
    if M >= 1024:
        G = M / 1024
        return "%fG" % (G)
    else:
        return "%.3fM" % (M)


# 获取文件大小
def getDocSize(path):
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        print(err)


# 获取文件夹大小
def getFileSize(path):
    sumsize = 0
    try:
        filename = os.walk(path)
        for root, dirs, files in filename:
            for fle in files:
                size = os.path.getsize(path + fle)
                sumsize += size
        return formatSize(sumsize)
    except Exception as err:
        print(err)
