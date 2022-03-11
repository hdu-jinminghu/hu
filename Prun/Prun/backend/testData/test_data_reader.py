'''
Author: your name
Date: 2021-11-19 09:28:09
LastEditTime: 2021-11-21 16:32:36
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \Prun\Prun\backend\testData\test_data_reader.py
'''

import base64
import os
from Prun.backend.utils import getPath
import json
def data_reader(job,dataset):
    image_path = getPath('./data/{}/image'.format(dataset))
    urls = []
    file_list = os.listdir(image_path)
    file_n = len(file_list)
    for i in range(file_n-1):
        f = open("{}/{}.jpg".format(image_path,i),"rb")
        base64_data = base64.b64encode(f.read())
        res = "data:image/png;base64,%s" % base64_data.decode()
        urls.append(res)
        f.close()
    res = []
    try:
        with open("{}/{}".format(image_path,"res.txt"),"r") as f:
            res = json.loads(f.readline())
    except Exception:
        res = []
    
    return {"data":urls,"res":res}
