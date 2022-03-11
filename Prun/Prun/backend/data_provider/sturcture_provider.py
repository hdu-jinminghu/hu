'''
Author: your name
Date: 2021-03-23 16:30:55
LastEditTime: 2021-12-13 21:59:32
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\data_provider\sturcture_provider.py
'''

import json
from .graph_read import get_data
import time
def graph_reader(request):
    job = request.GET.get("job")
    pos = request.GET.get("modelId")
    type = request.GET.get("type")
    prun = request.GET.get("prun")
    print(job)
    structure_path = "Prun/data/{}/{}/structure.json".format(job,pos)
    
    kernel_path = "Prun/data/{}/{}/kernel_size.json".format(job,pos)
    if type == "kernel":
        path = "Prun/data/{}/control.txt".format(job)
        
        with open(path,"r") as f:
            data = f.readline().strip()
            cSegs = data.split("@")
            sPath = cSegs[10]
            seg = sPath.split("/")
            # index = seg[-1]
            if prun:
                seg.append("kernel_size.json")
            else:
                seg[-1] = "kernel_size.json"
            print("********************************************************")
            print(cSegs)
            print("********************************************************")
            # if index == "0":
            #     seg.pop()
            #     seg[-1] = "kernel_size.json"
            #     kernel_path = "/".join(seg)
            # else:
            #     seg[-1] = str(int(seg[-1])-1)
            #     seg.pop()
            #     seg.pop()
            #     seg.append("kernel_size.json")
            kernel_path = "/".join(seg)
        while True:
            try:
                with open(kernel_path) as f:
                    kernel_data = json.load(f)
                break
            except Exception as e:
                time.sleep(0.5)
            
        return {"structure":"None", "kernel":kernel_data,"path":kernel_path}
                
            
            
            
    structure = []
    with open(structure_path) as f:
        structure_data = json.load(f)
    structure = get_data(structure_data)
    # print(structure)
    with open(kernel_path) as f:
        kernel_data = json.load(f)
    res = {"structure":structure, "kernel":kernel_data}
    return res

def layern(node,pattern=None):
    if pattern == "deep":
        if len(node.sub_net) == 0:
            node.layern = 0
        
    else:
        node.layern = len(node.sub_net)
        for i in node.sub_net:
            layern(i)