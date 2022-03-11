from collections import defaultdict 
import json
import torch.nn as nn
import torch
import torch.nn.functional as F

from tensorboardX import SummaryWriter

class MakeLayers():
    @staticmethod
    def conv2d(attr):
        return nn.Conv2d(in_channels=attr["in_channels"], 
                            out_channels=attr["out_channels"],
                            kernel_size=attr["kernel_size"],
                            stride=attr["stride"],
                            padding=attr["padding"],
                            bias=attr["bias"])
    @staticmethod
    def conv1d(attr):
        return nn.Conv1d(in_channels=attr["in_channels"], 
                            out_channels=attr["out_channels"],
                            kernel_size=attr["kernel_size"],
                            stride=attr["stride"],
                            padding=attr["padding"],
                            bias=attr["bias"])
    @staticmethod
    def bn2d(attr):
        return nn.BatchNorm2d(num_features=attr['num_features'])
    @staticmethod
    def bn1d(attr):
        return nn.BatchNorm1d(num_features=attr['num_features'])
    @staticmethod
    def linear(attr):
        return nn.Linear(in_features=attr["in_features"],
                            out_features=attr["out_features"],
                            bias=attr["bias"])
    @staticmethod
    def relu(attr):
        return nn.ReLU()
    @staticmethod
    def maxpool2d(attr):
        return nn.MaxPool2d(kernel_size=attr['kernel_size'],
                            stride=attr['stride'],
                            padding=attr['padding'],
                            return_indices=attr['return_indices'],
                            ceil_mode=attr["ceil_mode"])
    @staticmethod
    def maxpool1d(attr):
        return nn.MaxPool1d(kernel_size=attr['kernel_size'],
                            stride=attr['stride'],
                            padding=attr['padding'],
                            return_indices=attr['return_indices'],
                            ceil_mode=attr["ceil_mode"])
    @staticmethod
    def tanh(attr):
        return nn.Tanh()
    @staticmethod
    def sigmoid(attr):
        return nn.Sigmoid()
    
    @staticmethod
    def avgpool2d(attr):
        return nn.AvgPool2d(kernel_size=attr['kernel_size'],
                            stride=attr['stride'],
                            padding=attr['padding'])
    
    @staticmethod
    def adaptiveavgpool2d(attr):
        return nn.AdaptiveAvgPool2d((1,1))

    @staticmethod
    def sequence(attr):
        return nn.Sequential()
    '''创建的网络层统一管理'''
    @staticmethod
    def makelayer(type,attr,uid):
        boolenSet = ["bias","ceil_mode"]
        for i in attr.keys():
            if i in boolenSet:
                attr[i] = True if attr[i] == "true" else False
            else:
                attr[i] = int(attr[i])
            
        module = MakeLayers().__getattribute__(type)(attr)
        module.uid = uid
        return module
    
    
    




class Model(nn.Module):
    def __init__(self, sData, Topo, moduleDic,graph):
        super(Model, self).__init__()
        '''输入图'''
        self.graph = graph
        '''拓扑''' 
        self.Topo = Topo
        '''已创建的模块'''
        self.moduleDic = moduleDic
        self.op_attr = {}
        self._make_layers(sData)
        # print(Topo,graph)
    def op_view(self,attr,x):
        return x.view(x.size(0), -1)
    
    def op_add(self,attr,x,y):
        return x+y
    
    def op_sampling(self,attr,x):
        return F.interpolate(x, size=[x.shape[2]-attr["diff"], x.shape[3]-attr["diff"]])
    
    def op_cat(self,attr,*x):
        # attrs = attr
        inputs = []
        for i in x:
            inputs.append(i)
        return torch.cat(inputs, dim=1)
    def forward(self, x):
        '''record记录每个模块的输出'''
        record = {}
        # print(self.Topo,record)
        for i in self.Topo:
            if len(self.graph[i]) == 0:
                i = i.split('/')[-1]
                if i in self.__dict__:
                    record['{}_out'.format(i)] = self[i](x)
                else:
                    record['{}_out'.format(i)] = self.__getattr__(i)(x)
            else:
                input_ = []
                for input in self.graph[i]:
                    input = input.split('/')[-1]
                    input_.append(record['{}_out'.format(input)])
                i = i.split('/')[-1]
                if i in self.__dict__:
                    record['{}_out'.format(i)] = self[i](self.op_attr[i],*input_)
                else:
                    record['{}_out'.format(i)] = self.__getattr__(i)(*input_)
        
        return record['{}_out'.format(self.Topo[-1].split('/')[-1])]
    
    def __setitem__(self, key, val):
        self.__dict__[key] = val
    
    def __getitem__(self, key):
        if key in self.__dict__.keys():
            return self.__dict__[key]
        else:
            return self.moduleDic[key]
    
    def _make_layers(self, sData):
        '''创建神经元'''
        '''模块使用torch定义的__setattr__储存'''
        '''__setattr__不储存算术操作'''
        '''算术操作使用自定义的__setitem__储存'''
        for node in sData:
            if node['type'] != 'child':
                if not 'op' in node['type']:
                    self.__setattr__(node['uid'],MakeLayers.makelayer(node['type'],node['attr'],node['uid']))
                else:
                    self[node['uid']] = self.__getattribute__(node['type'])
                    self.op_attr[node['uid']] = node['attr']
            else:
                module = node['moduleId'].split('/')[-1]
                self.__setattr__(module,self.moduleDic[node['moduleId']])
            
        
        
        

'''拓扑排序'''
'''graph = {
    "F": [],
    "D": ["F"],
    "C": ["D","E"],
    "A": ["B","C"],
    "B": ["D","E"],
    "E": ["F"],
}
# print(TopologicalSort(graph))
['A', 'B', 'C', 'D', 'E', 'F']
'''
def TopologicalSort(G):
    ''' 创建入度字典 '''
    in_degrees = dict((u, 0) for u in G)
    ''' 获取每个节点的入度 '''
    for u in G:
        for v in G[u]:
            in_degrees[v] += 1
    ''' 使用列表作为队列并将入度为0的添加到队列中 '''
    Q = [u for u in G if in_degrees[u] == 0]
    res = []
    ''' 当队列中有元素时执行 '''
    while Q:
        ''' 从队列首部取出元素 '''
        u = Q.pop(0)
        ''' 将取出的元素存入结果中 '''
        res.append(u)
        ''' 移除与取出元素相关的指向，即将所有与取出元素相关的元素的入度减少1 '''
        for v in G[u]:
            in_degrees[v] -= 1
            ''' 若被移除指向的元素入度为0，则添加到队列中 '''
            if in_degrees[v] == 0:
                Q.append(v)
    return res

'''节点分组(模块)'''
def groupByModuleId(sData):
    group = {}
    for node in sData:
        segs = sData[node]['moduleId'].split('/')
        '''分配节点所属模块'''
        segs.pop()
        moduleId = "/".join(segs)
        if moduleId in group:
            group[moduleId].append(sData[node])
        else:
            group[moduleId] = [sData[node]]
    return group

'''子模块分组'''
def groupChildModule(groupData):
    moduleIdList = list(groupData.keys())
    moduleIdList.sort(key=lambda x:-len(x.split('/')))
    for i in range(len(moduleIdList)-1):
        segs = moduleIdList[i].split('/')
        segs.pop()
        anceModule = '/'.join(segs)
        inputs = []
        outputs = []
        uids = []
        '''收集子模块内所有输入输出'''
        for node in groupData[moduleIdList[i]]:
            inputs.extend(node["inputs"])
            outputs.extend(node["outputs"])
            if isinstance(node['uid'], str):
                uids.append(node['uid'])
            else:
                uids.extend(node['uid'])
        inputs = list(set(inputs))
        outputs = list(set(outputs))
        uids = list(set(uids))
        groupData[anceModule].append({'inputs':inputs,'outputs':outputs,'moduleId':moduleIdList[i],'type':'child','attr':{},'uid':uids})
    return groupData

'''模块创建'''
def createConnection(data,moduleId,moduleDic):
    '''建立拓扑结构'''
    graph = {}
    childs = {}
    '''储存所有节点和子模块'''
    for node in data:
        if node["type"] == 'child':
            childs[node['moduleId']] = node
            graph[node['moduleId']] = []
        else:
            graph[node['uid']] = []
    '''建立模块内节点间连接关系'''
    for node in data:
        if node['type'] != 'child':
            for output in node["outputs"]:
                if output in graph:
                    graph[node["uid"]].append(output)
    '''建立模块内节点和子模块间连接关系'''
    for child in childs.keys():
        for input in childs[child]['inputs']:
            if input in graph:
                graph[input].append(child)
        for output in childs[child]['outputs']:
            if output in graph:
                graph[child].append(output)
    '''建立子模块之间连接关系'''
    for child in childs.keys():
        for input in childs[child]['inputs']:
            for child_ in childs.keys():
                if child_ == child:
                    continue
                if input in childs[child_]['uid']:
                    graph[childs[child_]['moduleId']].append(child)
    topo = TopologicalSort(graph)
    return topo,graph
    
    
'''模型数据读取'''
def readSData(path):
    sData = {}
    with open(path, "r") as f:
        try:
            sData = json.loads(f.readline())
        except Exception:
            sData = {}
    # print(path)
    # print(sData)
    for nodeId in sData.keys():
        sData[nodeId]["uid"] = nodeId
        # sData[nodeId]["moduleId"] = sData[nodeId]["moduleId"][0] if sData[nodeId]["moduleId"][0] == '/' else '/{}'.format(sData[nodeId]["moduleId"])
        sData[nodeId]["outputs"] = []
        # print(sData[nodeId])
    for nodeId in sData.keys():
        for input in sData[nodeId]["inputs"]:
            sData[input]["outputs"].append(nodeId)
    # # print(sData)
    return sData
'''输出关系图->输入关系图'''
def changeGraph(graph):
    graph_ = {}
    for node in graph:
        graph_[node] = []
    for node in graph:
        for output in graph[node]:
            graph_[output].append(node)
    return graph_

'''模型创建'''
def createModel(path):
    sData = readSData(path)
    '''结构数据按模块名分组'''
    # print(sData)
    groupData = groupByModuleId(sData)
    # for i in groupData.keys():
    #     print(i,groupData[i])
    # print(groupData.keys())
    '''子模块分组'''
    groupData = groupChildModule(groupData)
    # for i in groupData.keys():
    #     print(i,groupData[i])
    # # print(groupData[''])
    '''moduleDic保存已创建的模块'''
    moduleDic = {}
    '''模块名排序'''
    moduleIdList = list(groupData.keys())
    moduleIdList.sort(key=lambda x:-len(x.split("/")))
    '''从底层开始搭建'''
    for moduleId in moduleIdList:
        '''确定模块连接顺序'''
        topo,graph = createConnection(groupData[moduleId],moduleId,moduleDic)
        '''输出关系图->输入关系图'''
        graph = changeGraph(graph)
        moduleDic[moduleId] = Model(groupData[moduleId],topo,moduleDic,graph)
    # # print(moduleDic.keys())
    return moduleDic['']
def reveal(module):
    # print(getattr(module, 'uid', 20))
        
    for i in module._modules.keys():
        tmpModule = module._modules[i]
        reveal(tmpModule)

def compile(basepath):
    write = SummaryWriter("{}/log".format(basepath))
    model = createModel("{}/model.json".format(basepath))
    write.add_graph(model, torch.randn([6,3,32,32]))
    return model

if __name__ == "__main__":
    write = SummaryWriter("./datab")
    # model = createModel("model.json")
    model = createModel("./model.json")
    # model = createModel("config.json")
    # print(model)
    # write.add_graph(model, torch.randn([3,3,64,64])) 
    # torch.save(model,"model.pt")
    # model1 = torch.load("model.pt",map_location='cuda:0')
    # reveal(model1)
    print(model)
    write.add_graph(model, torch.randn([6,3,32,32]))
    # # print(model)
    
