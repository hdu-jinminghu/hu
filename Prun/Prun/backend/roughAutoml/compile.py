'''
模型构建
'''
from collections import defaultdict 
import json
import torch.nn as nn
import torch
from tensorboardX import SummaryWriter
import torch.nn.functional as F


SYMBOL = '*'

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
                            stride=int(attr['stride']),
                            padding=int(attr['padding']))
    @staticmethod
    def maxpool1d(attr):
        return nn.MaxPool1d(kernel_size=attr['kernel_size'],
                            stride=attr['stride'],
                            padding=attr['padding'],)
    @staticmethod
    def tanh(attr):
        return nn.Tanh()
    @staticmethod
    def sigmoid(attr):
        return nn.Sigmoid()
    @staticmethod
    def adaptiveavgpool2d(attr):
        return nn.AdaptiveAvgPool2d((1,1))
    @staticmethod
    def avgpool2d(attr):
        return nn.AvgPool2d(kernel_size=attr['kernel_size'],
                            stride=attr['stride'],
                            padding=attr['padding'])
    @staticmethod
    def sequence(attr):
        return nn.Sequential()
    '''创建的网络层统一管理'''
    @staticmethod
    def makelayer(type,attr,uid):
        boolenSet = ["bias","ceil_mode","return_indices"]
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
        
    def op_view(self,attr,x):
        return x.view(x.size(0), -1)
    
    def op_add(self,attr,*x):
        
        return sum(x)
    
    def op_cat(self,attr,*x):
        # attrs = attr
        inputs = []
        for i in x:
            inputs.append(i)
        return torch.cat(inputs, dim=1)
    
    def op_sampling(self,attr,x):
        return F.interpolate(x, size=[x.shape[2]-attr["diff"], x.shape[3]-attr["diff"]])
    
    def forward(self, x):
        '''record记录每个模块的输出'''
        record = {}
        record['source_out'] = x
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
        elif key in self.moduleDic.keys():
            return self.moduleDic[key]
    
    def _make_layers(self, sData):
        '''创建神经元'''
        '''模块使用torch定义的__setattr__储存'''
        '''__setattr__不储存算术操作'''
        '''算术操作使用自定义的__setitem__储存'''
        for node in sData:
            if node['type'] == "input" or node['type'] == 'output':
                continue
            if node['type'] != 'child':
                if not 'op' in node['type']:
                    self.__setattr__(node['uid'],MakeLayers.makelayer(node['type'],node['attrs'],node['uid']))
                else:
                    self[node['uid']] = self.__getattribute__(node['type'])
                    self.op_attr[node['uid']] = node['attrs']
            else:
                module = node['uid'].split('/')[-1]
                self.__setattr__(module,self.moduleDic[node['uid']])
        print("build successful")
            
        
        
        

'''拓扑排序'''
'''graph = {
    "F": [],
    "D": ["F"],
    "C": ["D","E"],
    "A": ["B","C"],
    "B": ["D","E"],
    "E": ["F"],
}
print(TopologicalSort(graph))
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
def reWriteId(sData):
    for id in sData.keys():
        for line in sData[id]['lineList']:
            # vertexArray = line['id'].split("-")
            # vertexArray[0] = "{}{}{}".format(id,SYMBOL,vertexArray[0])
            # vertexArray[1] = "{}{}{}".format(id,SYMBOL,vertexArray[1])
            # line['id'] = '-'.join(vertexArray)
            # line['from'] = vertexArray[0]
            # line['to'] = vertexArray[1]
            line['from'] = "{}{}{}".format(id,SYMBOL,line['from'])
            line['to'] = "{}{}{}".format(id,SYMBOL,line['to'])
            line['id'] = "{}-{}".format(line['from'],line['to'])
            
        for node in sData[id]['nodeList']:
            node['id'] = "{}{}{}".format(id,SYMBOL,node['id'])


'''模块创建'''
def createConnection(data):
    '''建立拓扑结构'''
    graph = {}
    point = []
    for line in data['lineList']:
        if line['from'] in graph:
            graph[line['from']].append(line['to'])
        else:
            graph[line['from']] = [line['to']]
        if not line['to'] in graph:
            graph[line['to']] = []
            
    topo = TopologicalSort(graph)
    return topo,graph
    
def dpsearch(vertex,path,dic):
    dic[path] = vertex
    for ver in vertex['nodeList']:
        ver['uid'] = "{}{}{}".format(path,SYMBOL,ver['id'])
        if 'nodeList' in ver:
            ver['type'] = 'child'
            dpsearch(ver,"{}{}{}".format(path,SYMBOL,ver['id']),dic)

'''模型数据读取,模块分组'''
def readSData(path):
    sData = {}
    groupVertex = {}
    with open(path, "r") as f:
        try:
            sData = json.loads(f.readline())
        except Exception:
            sData = {}
    dpsearch(sData,'',groupVertex)
    return groupVertex

'''输出关系图->输入关系图'''
def changeGraph(graph):
    graph_ = {}
    for node in graph:
        graph_[node] = []
    for node in graph:
        for output in graph[node]:
            graph_[output].append(node)
    return graph_
'''节点记录'''
def recordVertex(graph):
    vertexRecord = {}
    for vertex in graph['nodeList']:
        vertexRecord[vertex['id']] = vertex
    return vertexRecord

'''模型创建'''
def createModel(path):
    '''模型数据读取,模块分组'''
    sData = readSData(path)
    '''重写网络节点id'''
    reWriteId(sData)
    
    moduleIdList = list(sData.keys())
    moduleIdList.sort(key=lambda x:-len(x.split(SYMBOL)))
    
    '''moduleDic保存已创建的模块'''
    moduleDic = {}
    # print(moduleIdList)
    '''从底层开始搭建'''
    for moduleId in moduleIdList:
        '''确定模块连接顺序'''
        topo,graph = createConnection(sData[moduleId])
        '''输出关系图->输入关系图'''
        graph = changeGraph(graph)
        
        for i in graph:
            for j in range(len(graph[i])):
                if graph[i][j] == topo[0]:
                    graph[i][j] = 'source'
                
        del graph[topo[-1]]
        del graph[topo[0]]
        del topo[0]
        del topo[-1]
        moduleDic[moduleId] = Model(sData[moduleId]['nodeList'],topo,moduleDic,graph)
    return moduleDic['']

# if __name__ == "__main__":
#     write = SummaryWriter("datab")
#     # model = createModel("model.json")
#     model = createModel("log/28/model.json")
#     print(model)
#     # write.add_graph(model, torch.randn([3,3,64,64])) 
#     # write.add_graph(model, torch.randn([1,3,64,64]))
    
#     # for i in model.named_parameters():
#     #     print(i[0])
#     for i in model.modules():
#         if hasattr(i,'uid'):
#             print(i.uid)
    
