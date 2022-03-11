import json
from compile import compile

'''
编辑模型文档
jsonPath：模型数据路径
nodeInfo:节点信息列表,{"1":[],"2":[],"3":[]},编辑类型->{'1':删除，'2':新增, '3':修改}
{"inputs":inputs,"outputs":outputs,"type":type,"moduleId":moduleId,"attr":attr,"uid":uid}

'''
class editModel():
    @staticmethod
    def exec(jsonPath,info):
        modelStruct = {}
        for node in info:
            modelStruct[node["uid"]] = node
        with open(jsonPath, "w") as f:
            f.write(json.dumps(modelStruct))
class editConfig():
    @staticmethod
    def exec(jsonPath,info):
        with open(jsonPath, "w") as f:
            f.write(json.dumps(info))

def edit(jsonPath, info):
    if jsonPath.endswith("config.json"):
        editConfig.exec(jsonPath, info)
    elif jsonPath.endswith("base.json"):
        editModel.exec(jsonPath, info)
        

conv = [
     {"inputs":[],"outputs":["layer2"],"type":"conv2d","moduleId":"/conv","attr":{"padding":0,"bias":True,"stride":1,"in_channels":3,"out_channels":6,"kernel_size":3},"uid":"layer1"},
     {"inputs":["layer1"],"outputs":["layer3"],"type":"bn2d","moduleId":"/bn","attr":{"num_features":6},"uid":"layer2"},
     {"inputs":["layer2"],"outputs":["layer4"],"type":"relu","moduleId":"/relu","attr":{'inplace':True},"uid":"layer3"},
     {"inputs":["layer3"],"outputs":["layer5"],"type":"conv2d","moduleId":"/conv","attr":{"padding":0,"bias":True,"stride":1,"in_channels":6,"out_channels":32,"kernel_size":3},"uid":"layer4"},
     {"inputs":["layer4"],"outputs":["layer6"],"type":"bn2d","moduleId":"/bn","attr":{"num_features":32},"uid":"layer5"},
     {"inputs":["layer5"],"outputs":["layer7"],"type":"relu","moduleId":"/relu","attr":{'inplace':True},"uid":"layer6"},
     {"inputs":["layer6"],"outputs":["layer8"],"type":"conv2d","moduleId":"/conv","attr":{"padding":0,"bias":True,"stride":1,"in_channels":32,"out_channels":64,"kernel_size":3},"uid":"layer7"},
     {"inputs":["layer7"],"outputs":["layer9"],"type":"bn2d","moduleId":"/bn","attr":{"num_features":64},"uid":"layer8"},
     {"inputs":["layer8"],"outputs":[],"type":"relu","moduleId":"/relu","attr":{'inplace':True},"uid":"layer9"},
     ]
# 配置
# 1：固定网络层；2.限制层间间隔;3.网络总层数
conv_config = {
    "fixed":["layer1","layer7"],
    "limitations":[["layer1","layer7",0,8]],
    "depth":[2,12]
}

resnet = [
    # {"inputs":[],"outputs":["2"],"type":"conv2d","moduleId":"/conv","attr":{"padding":1,"bias":True,"stride":1,"in_channels":3,"out_channels":6,"kernel_size":3},"uid":"1"},
    #  {"inputs":["1"],"outputs":["3"],"type":"bn2d","moduleId":"/bn","attr":{"num_features":6},"uid":"2"},
    #  {"inputs":["2"],"outputs":["113"],"type":"relu","moduleId":"/relu","attr":{'inplace':True},"uid":"3"},
     
    #  {"inputs":["3"],"outputs":["4"],"type":"sequence","moduleId":"/sequence","attr":{},"uid":"113"},
     
     {"inputs":[],"outputs":["5"],"type":"conv2d","moduleId":"/conv","attr":{"padding":1,"bias":True,"stride":1,"in_channels":6,"out_channels":6,"kernel_size":3},"uid":"4"},
     {"inputs":["4"],"outputs":["6"],"type":"bn2d","moduleId":"/bn","attr":{"num_features":6},"uid":"5"},
     {"inputs":["5"],"outputs":["7","13"],"type":"relu","moduleId":"/relu","attr":{'inplace':True},"uid":"6"},
     {"inputs":["6"],"outputs":["8"],"type":"conv2d","moduleId":"/conv","attr":{"padding":1,"bias":True,"stride":1,"in_channels":6,"out_channels":6,"kernel_size":3},"uid":"7"},
     {"inputs":["7"],"outputs":["9"],"type":"bn2d","moduleId":"/bn","attr":{"num_features":6},"uid":"8"},
     {"inputs":["8"],"outputs":["10"],"type":"relu","moduleId":"/relu","attr":{'inplace':True},"uid":"9"},
     {"inputs":["9","14"],"outputs":[],"type":"op_add","moduleId":"/add","attr":{},"uid":"10"},
     
     {"inputs":["6"],"outputs":["14"],"type":"conv2d","moduleId":"/conv2d","attr":{"padding":0,"bias":True,"stride":1,"in_channels":6,"out_channels":6,"kernel_size":1},"uid":"13"},
     {"inputs":["13"],"outputs":["10"],"type":"op_sampling","moduleId":"/op_sampling","attr":{"diff":0},"uid":"14"},
     
     ]

test = [{'inputs': [], 'outputs': ['layer11/layer4'], 'type': 'conv2d', 'moduleId': '/layer11/conv2d', 'attr': {'in_channels': '6', 'out_channels': '6', 'kernel_size': '3', 'stride': '1', 'padding': '1', 'bias': 'false'}, 'uid': 'layer11/layer3'}, 
        {'inputs': ['layer11/layer3'], 'outputs': ['layer11/layer5'], 'type': 'bn2d', 'moduleId': '/layer11/bn2d', 'attr': {'num_features': '6'}, 'uid': 'layer11/layer4'}, 
        {'inputs': ['layer11/layer4'], 'outputs': [], 'type': 'relu', 'moduleId': '/layer11/relu', 'attr': {}, 'uid': 'layer11/layer5'}]

test_ = [{"inputs": [], "outputs": ["9"], "type": "conv2d", "moduleId": "/conv2d", "attr": {"in_channels": "3", "out_channels": "6", "kernel_size": "3", "stride": "1", "padding": "1", "bias": "false"}, "uid": "8"}, 
        {"inputs": ["8"], "outputs": ["10"], "type": "bn2d", "moduleId": "/bn2d", "attr": {"num_features": "6"}, "uid": "9"}, 
        {"inputs": ["9"], "outputs": ["113"], "type": "relu", "moduleId": "/relu", "attr": {}, "uid": "10"}, 
        # {"inputs": ["125"], "outputs": ["14"], "type": "op_view", "moduleId": "/op_view", "attr": {}, "uid": "13"}, 
        # {"inputs": ["13"], "outputs": [], "type": "linear", "moduleId": "/linear", "attr": {"in_features": "54", "out_features": "1", "bias": "false"}, "uid": "14"},
        {"inputs": ["10"], "outputs": ["114"], "type": "conv2d", "moduleId": "layer11/conv2d", "attr": {"in_channels": "6", "out_channels": "6", "kernel_size": "3", "stride": "1", "padding": "1", "bias": "false"}, "uid": "113"}, 
        {"inputs": ["113"], "outputs": ["115"], "type": "bn2d", "moduleId": "layer11/bn2d", "attr": {"num_features": "6"}, "uid": "114"}, 
        {"inputs": ["114"], "outputs": ["123"], "type": "relu", "moduleId": "layer11/relu", "attr": {}, "uid": "115"}, 
        {"inputs": ["115"], "outputs": [], "type": "conv2d", "moduleId": "layer12/conv2d", "attr": {"in_channels": "6", "out_channels": "6", "kernel_size": "3", "stride": "1", "padding": "1", "bias": "false"}, "uid": "123"},
        # {"inputs": ["123"], "outputs": ["125"], "type": "bn2d", "moduleId": "layer12/bn2d", "attr": {"num_features": "6"}, "uid": "124"}, 
        # {"inputs": ["124"], "outputs": [], "type": "relu", "moduleId": "layer12/relu", "attr": {}, "uid": "125"}
        ]

test__ = [{"inputs": [], "outputs": ["9"], "type": "conv2d", "moduleId": "/conv2d", "attr": {"in_channels": "3", "out_channels": "6", "kernel_size": "3", "stride": "1", "padding": "1", "bias": "false"}, "uid": "8"}, 
        {"inputs": ["8"], "outputs": ["10"], "type": "bn2d", "moduleId": "/bn2d", "attr": {"num_features": "6"}, "uid": "9"}, 
        {"inputs": ["9"], "outputs": ["113"], "type": "relu", "moduleId": "/relu", "attr": {}, "uid": "10"}, 
        {"inputs": ["115"], "outputs": ["14"], "type": "op_view", "moduleId": "/op_view", "attr": {}, "uid": "13"}, 
        {"inputs": ["13"], "outputs": [], "type": "linear", "moduleId": "/linear", "attr": {"in_features": "54", "out_features": "1", "bias": "false"}, "uid": "14"},
        {"inputs": ["10"], "outputs": ["114"], "type": "conv2d", "moduleId": "layer11/conv2d", "attr": {"in_channels": "6", "out_channels": "6", "kernel_size": "3", "stride": "1", "padding": "1", "bias": "false"}, "uid": "113"}, 
        {"inputs": ["113"], "outputs": ["115"], "type": "bn2d", "moduleId": "layer11/bn2d", "attr": {"num_features": "6"}, "uid": "114"}, 
        {"inputs": ["114"], "outputs": ["13"], "type": "relu", "moduleId": "layer11/relu", "attr": {}, "uid": "115"}, ]
# for i in test_:
#     for j in range(len(i["inputs"])):
#         i["inputs"][j] = i["inputs"][j][-1] + str(len(i["inputs"][j]))
#     for j in range(len(i["outputs"])):
#         i["outputs"][j] = i["outputs"][j][-1] + str(len(i["outputs"][j]))
#     i["uid"] = i["uid"][-1] + str(len(i["uid"]))
# t = [{'inputs': [], 'outputs': ['96'], 'type': 'conv2d', 'moduleId': '/conv2d', 'attr': {'in_channels': '3', 'out_channels': '6', 'kernel_size': '3', 'stride': '1', 'padding': '1', 'bias': 'false'}, 'uid': '86'}, {'inputs': ['86'], 'outputs': ['07'], 'type': 'bn2d', 'moduleId': '/bn2d', 'attr': {'num_features': '6'}, 'uid': '96'}, {'inputs': ['96'], 'outputs': ['314'], 'type': 'relu', 'moduleId': '/relu', 'attr': {}, 'uid': '07'}, {'inputs': ['514'], 'outputs': ['47'], 'type': 'op_view', 'moduleId': '/op_view', 'attr': {}, 'uid': '37'}, {'inputs': ['37'], 'outputs': [], 'type': 'linear', 'moduleId': '/linear', 'attr': {'in_features': '54', 'out_features': '1', 'bias': 'false'}, 'uid': '47'}, {'inputs': ['07'], 'outputs': ['414'], 'type': 'conv2d', 'moduleId': 'layer11/conv2d', 'attr': {'in_channels': '6', 'out_channels': '6', 'kernel_size': '3', 'stride': '1', 'padding': '1', 'bias': 'false'}, 'uid': '314'}, {'inputs': ['314'], 'outputs': ['514'], 'type': 'bn2d', 'moduleId': 'layer11/bn2d', 'attr': {'num_features': '6'}, 'uid': '414'}, {'inputs': ['414'], 'outputs': ['314'], 'type': 'relu', 'moduleId': 'layer11/relu', 'attr': {}, 'uid': '514'}, {'inputs': ['514'], 'outputs': ['414'], 'type': 'conv2d', 'moduleId': 'layer12/conv2d', 'attr': {'in_channels': '6', 'out_channels': '6', 'kernel_size': '3', 'stride': '1', 'padding': '1', 'bias': 'false'}, 'uid': '314'}, {'inputs': ['314'], 'outputs': ['514'], 'type': 'bn2d', 'moduleId': 'layer12/bn2d', 'attr': {'num_features': '6'}, 'uid': '414'}, {'inputs': ['414'], 'outputs': ['37'], 'type': 'relu', 'moduleId': 'layer12/relu', 'attr': {}, 'uid': '514'}]
t = [
    {'inputs': [], 'outputs': ['layer2'], 'type': 'conv2d', 'moduleId': '/conv', 'attr': {'padding': 0, 'bias': True, 'stride': 1, 'in_channels': 3, 'out_channels': 6, 'kernel_size': 3}, 'uid': 'layer1'},
    {'inputs': ['layer1'], 'outputs': ['layer3'], 'type': 'bn2d', 'moduleId': '/bn', 'attr': {'num_features': 6}, 'uid': 'layer2'},
    {'inputs': ['layer2'], 'outputs': ['epoch7_layer7'], 'type': 'relu', 'moduleId': '/relu', 'attr': {'inplace': True}, 'uid': 'layer3'},
    {'inputs': ['epoch7_layer9'], 'outputs': ['layer8'], 'type': 'conv2d', 'moduleId': '/conv', 'attr': {'padding': 0, 'bias': True, 'stride': 1, 'in_channels': 6, 'out_channels': 64, 'kernel_size': 3}, 'uid': 'layer7'},
    {'inputs': ['layer7'], 'outputs': ['layer9'], 'type': 'bn2d', 'moduleId': '/bn', 'attr': {'num_features': 64}, 'uid': 'layer8'},
    {'inputs': ['layer8'], 'outputs': [], 'type': 'relu', 'moduleId': '/relu', 'attr': {'inplace': True}, 'uid': 'layer9'},
    {'attr': {'padding': 0, 'bias': True, 'stride': 1, 'in_channels': 6, 'out_channels': 6, 'kernel_size': 3}, 'inputs': ['layer3'], 'type': 'conv2d', 'moduleId': '/conv2d', 'uid': 'epoch7_layer7', 'outputs': ['epoch7_layer8']},
    {'attr': {'num_features': 6}, 'inputs': ['epoch7_layer7'], 'type': 'bn2d', 'moduleId': '/bn2d', 'uid': 'epoch7_layer8', 'outputs': ['epoch7_layer9']},
    {'attr': {}, 'inputs': ['epoch7_layer8'], 'type': 'relu', 'moduleId': '/relu', 'uid': 'epoch7_layer9', 'outputs': ['layer7']}
    ]

goo = [{"inputs":[],"outputs":["2"],"type":"conv2d","moduleId":"/conv","attr":{"padding":1,"bias":True,"stride":1,"in_channels":3,"out_channels":6,"kernel_size":3},"uid":"1"},
     {"inputs":["1"],"outputs":["3"],"type":"bn2d","moduleId":"/bn","attr":{"num_features":6},"uid":"2"},
     {"inputs":["2"],"outputs":["4"],"type":"relu","moduleId":"/relu","attr":{'inplace':True},"uid":"3"},
     
     
     {"inputs":["3"],"outputs":["5"],"type":"conv2d","moduleId":"/conv","attr":{"padding":1,"bias":True,"stride":1,"in_channels":6,"out_channels":2,"kernel_size":3},"uid":"4"},
     {"inputs":["4"],"outputs":["6"],"type":"bn2d","moduleId":"/bn","attr":{"num_features":2},"uid":"5"},
     {"inputs":["5"],"outputs":["13"],"type":"relu","moduleId":"/relu","attr":{'inplace':True},"uid":"6"},
     
     {"inputs":["3"],"outputs":["8"],"type":"conv2d","moduleId":"/conv","attr":{"padding":1,"bias":True,"stride":1,"in_channels":6,"out_channels":2,"kernel_size":3},"uid":"7"},
     {"inputs":["7"],"outputs":["9"],"type":"bn2d","moduleId":"/bn","attr":{"num_features":2},"uid":"8"},
     {"inputs":["8"],"outputs":["13"],"type":"relu","moduleId":"/relu","attr":{'inplace':True},"uid":"9"},
     
     {"inputs":["3"],"outputs":["11"],"type":"conv2d","moduleId":"/conv","attr":{"padding":1,"bias":True,"stride":1,"in_channels":6,"out_channels":2,"kernel_size":3},"uid":"10"},
     {"inputs":["10"],"outputs":["12"],"type":"bn2d","moduleId":"/bn","attr":{"num_features":2},"uid":"11"},
     {"inputs":["11"],"outputs":["13"],"type":"relu","moduleId":"/relu","attr":{'inplace':True},"uid":"12"},
     
     {"inputs":["6","9","12"],"outputs":["14"],"type":"op_cat","moduleId":"/cat","attr":{},"uid":"13"},
     
     {"inputs":["13"],"outputs":["15"],"type":"op_view","moduleId":"/view","attr":{},"uid":"14"},
     {"inputs":["14"],"outputs":[],"type":"linear","moduleId":"/linear","attr":{"in_features":6144,"out_features":1,"bias":True},"uid":"15"},
     ]

edit("base.json",conv)
edit("config.json",conv_config)





