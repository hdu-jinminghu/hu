'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2021-12-10 15:59:55
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import numpy as np
import json
import os
import json
import trace
from Prun.backend.utils import getPath,getFileSize
def automl_graph_reader(model_id):

    graphpath = getPath("Prun/automl/{}/model.json".format(model_id))
    graph = None
    with open(graphpath,"r") as f:
        graph = json.load(f)
    lineList = []
    nodeList = []
    for key in graph.keys():
        nvertex = {}
        vertex = graph[key]
        nvertex["attrs"] = vertex["attr"]
        nvertex["id"] = vertex["uid"]
        nvertex["type"] = vertex["type"]
        nvertex["typeName"] = vertex["type"]
        nvertex["log_bg_color"] = "rgba(0, 128, 0, 0.2)"
        nvertex["nodeName"] = vertex["type"]
        nodeList.append(nvertex)
        for output in vertex["outputs"]:
            line = {}
            line["Remark"] = ""
            line["from"] = vertex["uid"]
            line["to"] = output
            line["label"] = '连线名称'
            line["id"] = '{}-{}'.format(vertex["uid"],output)
            lineList.append(line)
        if len(vertex["outputs"]) == 0:
            output = {}
            output["attrs"] = {}
            output["id"] = "exit"
            output["type"] = "output"
            output["typeName"] = "output"
            output["log_bg_color"] = "rgba(0, 128, 0, 0.2)"
            output["nodeName"] = "output"
            nodeList.append(output)
            line = {}
            line["Remark"] = ""
            line["from"] = vertex["uid"]
            line["to"] = "exit"
            line["label"] = '连线名称'
            line["id"] = '{}-{}'.format(vertex["uid"],"exit")
            lineList.append(line)
        if len(vertex["inputs"]) == 0:
            input = {}
            input["attrs"] = {}
            input["id"] = "enter"
            input["type"] = "input"
            input["typeName"] = "input"
            input["log_bg_color"] = "rgba(0, 128, 0, 0.2)"
            input["nodeName"] = "input"
            nodeList.append(input)
            line = {}
            line["Remark"] = ""
            line["from"] = "enter"
            line["to"] = vertex["uid"]
            line["label"] = '连线名称'
            line["id"] = '{}-{}'.format("enter",vertex["uid"])
            lineList.append(line)

        
    return {"nodeList":nodeList, "lineList":lineList}

