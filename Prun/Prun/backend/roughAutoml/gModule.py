from .template import *
import re
import json
import random
import math
from .compile import createModel
import torch
import torch.onnx
import os
from torch.autograd import Variable
from .train import *
REGEX = re.compile("\[(\d+)\]")
LEVEL0_ENTITY = []
LEVEL1_ENTITY = [None for _ in range(len(LEVEL_1))]




# level0:基本操作 {"lineList":[],"nodeList":[]}
# level1:初步组装 {"lineList":[],"nodeList":[]}
# level2:最终模块 {"lineList":[],"nodeList":[],"channels":x}
class model:
    def __init__(self,level1,level2):
        self.level0 = LEVEL_0
        self.level1 = json.loads(json.dumps(level1))
        self.level2 = json.loads(json.dumps(level2))
        # for i in level2:
        #     print(i['channels'])
        #     print("========================================================================================================")
        #     for node in i['nodeList']:
        #         print(node)
        #     print("--------------------------------------------------------------------------------------------------------")
        #     for line in i['lineList']:
        #         print(line)
        self.LEVEL1_ENTITY = [None for _ in range(len(level1))]
        self.LEVEL2_ENTITY = [None for _ in range(len(level2))]
    # 变异
    def vary(self):
        while True:
            choice = random.choices([1,2])[0]
            r = self.replace(choice)
            if r:
                break
    
    # 替换节点
    # 1、选择目标targetLevel中一个模板
    # 2、选择模板中一个节点替换
    def replace(self,choice):
        targetLevel = None
        toolLevel = None
        
        if choice == 1:
            targetLevel = self.level1
            toolLevel = self.level0
        elif choice == 2:
            targetLevel = self.level2
            toolLevel = self.level1
            
        # 可替换节点
        vertexAbleList = []
        # 随机目标模板
        randomIndex = random.choice(range(len(targetLevel)))
        subnet = targetLevel[randomIndex]
        
        for vertex in subnet['nodeList']:
            if vertex['type'].startswith("level"):
                vertexAbleList.append(vertex)
        # print(vertexAbleList)
        if len(vertexAbleList) == 0:
            return False
        target = random.choices(vertexAbleList)[0]
        # 可使用节点
        vertexChoices = list(range(len(toolLevel)))
        while True:
            vertex = random.choices(vertexChoices)[0]
            index = int(REGEX.findall(target['type'])[0])
            if vertex != index:
                type = "level{}[{}]".format(choice-1,vertex)
                target["type"] = type
                target["nodeName"] = type
                target["typeName"] = type
                break
        return True
        
        
    # 组装level0,level1,level2
    def assemble(self):
        # 拼接level1
        for level1PartIndex in range(len(self.level1)):
            graph = self.embed(self.level1[level1PartIndex],self.level0)
            self.LEVEL1_ENTITY[level1PartIndex] = graph
        # 拼接level2
        for level2PartIndex in range(len(self.level2)):
            for vertex in self.level2[level2PartIndex]["nodeList"]:
                if vertex['type'].startswith("level"):
                    lowerIndex = int(REGEX.findall(vertex['type'])[0])
                    # print(vertex)
                    # print(self.LEVEL1_ENTITY[lowerIndex]["lineList"])
                    vertex["lineList"] = json.loads(json.dumps(self.LEVEL1_ENTITY[lowerIndex]["lineList"]))
                    vertex["nodeList"] = json.loads(json.dumps(self.LEVEL1_ENTITY[lowerIndex]["nodeList"]))
                    self.setAttrs(vertex,self.level2[level2PartIndex]["channels"])
            # graph = self.embed(self.level2[level2PartIndex],self.LEVEL1_ENTITY)
            # self.setAttrs(graph,self.level2[level2PartIndex]["channels"])
            # graph["type"] = self.level2[level2PartIndex]["type"]
                self.LEVEL2_ENTITY[level2PartIndex] = self.level2[level2PartIndex]
            
        # for line in graph["lineList"]:
        #     print("line",line)
        # print("****************************************************")
        # for node in graph["nodeList"]:
        #     print("node",node)
        
    # 低级模块嵌入高级模块
    # 嵌入后的实例放入高级模块实例列表，方便后续重复使用
    def embed(self,higher,lower):
        # 拷贝，在拷贝上修改
        higherCopy = json.loads(json.dumps(higher))
        account = 0

        for vertex in higher["nodeList"]:
            # 判断模块节点
            if vertex['type'].startswith("level"):
                # 查找对应低级模块,拷贝
                lowerIndex = int(REGEX.findall(vertex['type'])[0])
                vertexCopy = json.loads(json.dumps(lower[lowerIndex]))
                # 修改名称避免重复
                for line in vertexCopy['lineList']:
                    line["from"] = "{}{}".format(line["from"],account)
                    line["to"] = "{}{}".format(line["to"],account)
                    line["id"] = "{}-{}".format(line["from"],line["to"])
                for node in vertexCopy["nodeList"]:
                    node["id"] = "{}{}".format(node["id"],account)
                
                # 低级模块内的出入口
                head,tail = self.getHeadTail(vertexCopy)
                # 拷贝插入具体网络
                # 拷贝中查找相应模块节点
                for index in range(len(higherCopy["nodeList"])):
                    v = higherCopy["nodeList"][index]
                    # 删除相应点
                    if v["id"] == vertex["id"]:
                        higherCopy["nodeList"].pop(index)
                        break
                # 模块节点网络插入，除input、output
                for v in vertexCopy["nodeList"]:
                    if v["type"] == "input" or v['type'] == "output":
                        continue
                    higherCopy["nodeList"].append(v)
                # 模块边插入，除input、output相关边
                for line in vertexCopy["lineList"]:
                    if line["from"] == list(head.keys())[0] or line['to'] == list(tail.keys())[0]:
                        continue
                    higherCopy["lineList"].append(line)
                    
                # 拷贝中查找相关边记录下标
                indexList = []
                for index in range(len(higherCopy["lineList"])):
                    line = higherCopy["lineList"][index]
                    if line["from"] == vertex["id"] or line["to"] == vertex["id"]:
                        indexList.append(index)
                # 插入边
                # 倒序遍历，避免删除后序号不一致
                for index in range(len(indexList)-1,-1,-1):
                    line = higherCopy["lineList"].pop(indexList[index])
                    # 输出边
                    if line["from"] == vertex["id"]:
                        for from_ in list(tail.values())[0]:
                            newLine = {
                                'Remark': '', 
                                'from': from_, 
                                'to': line["to"], 
                                'label': '连线名称', 
                                'id': '{}-{}'.format(from_,line['to'])
                            }
                            higherCopy["lineList"].append(newLine)
                    # 输入边
                    if line["to"] == vertex["id"]:
                        for to_ in list(head.values())[0]:
                            newLine = {
                                'Remark': '', 
                                'from': line["from"], 
                                'to': to_, 
                                'label': '连线名称', 
                                'id': '{}-{}'.format(line["from"],to_)
                            }
                            higherCopy["lineList"].append(newLine)
            account += 1
        return higherCopy
    
    # 查找模块输入口、输出口
    # 返回输入口输出口以及关联节点
    def getHeadTail(self,graph):
        forwardGraph = {}
        backwardGraph = {}
        tail = None
        head = None
        for line in graph["lineList"]:
            if line["from"] in forwardGraph:
                forwardGraph[line["from"]].append(line["to"])
            else:
                forwardGraph[line["from"]] = [line["to"]]
            if not line["to"] in forwardGraph:
                forwardGraph[line["to"]] = []
            
            if line["to"] in backwardGraph:
                backwardGraph[line["to"]].append(line["from"])
            else:
                backwardGraph[line["to"]] = [line["from"]]
            if not line["from"] in backwardGraph:
                backwardGraph[line["from"]] = []
            
        for vertex in forwardGraph.keys():
            if len(forwardGraph[vertex]) == 0:
                tail = vertex
                break
        
        for vertex in backwardGraph.keys():
            if len(backwardGraph[vertex]) == 0:
                head = vertex
                break
            
        return ({head:forwardGraph[head]},{tail:backwardGraph[tail]})
    
    # 初始化通道
    def setAttrs(self,graph,channels):
        # 记录节点、cat节点、拓扑图
        vertexDic = {}
        catOperationList = []
        topoGraph = {}
        # 统一修改通道
        for v in graph["nodeList"]:
            if "num_features" in v["attrs"]:
                v["attrs"]["num_features"] = channels
            elif "in_channels" in v["attrs"]:
                v["attrs"]["in_channels"] = channels
                v["attrs"]["out_channels"] = channels
            vertexDic[v["id"]] = v
            if v["type"] == "op_cat":
                catOperationList.append(v["id"])
        # print(catOperationList)
        # 修改特殊节点通道
        # 1.拓扑图
        # for line in graph["lineList"]:
        #     if line["to"] in topoGraph:
        #         topoGraph[line['to']].append(line['from'])
        #     else:
        #         topoGraph[line['to']] = [line['from']]
        #     if line['from'] not in topoGraph:
        #         topoGraph[line['from']] = []
        # 2.遍历
        # 通道 x1=channels/3 x2=channels/3 x3=channels-x1-x2
        # for catVertex in catOperationList:    
            

# moduleList:[{"channels":8,"deepth":10,"type":"xxx",},{"channels":50,"deepth":6,"type":"yyy"}]
class Factory():
    def __init__(self,level0,level1,skelen,moduleList,epoch):
        self.account = 0
        self.limit = 100
        self.skelen = skelen
        self.level0 = level0
        self.level1 = level1
        self.level2 = []
        self.moduleList = moduleList
        self.population = []
        self.epoch = epoch

    # 生成原始模板
    def produceOrigin(self,moduleList):
        for module in moduleList:
            template = [
                {"outputs":[],"type":"input","attr":{},"uid":"vertex0"},
            ]
            for i in range(0,math.ceil(int(module["deepth"]))):
                vertex = {"outputs":[],"type":"level1[1]","attr":{},"uid":"vertex2"}
                vertex["uid"] = "vertex{}".format(i+1)
                template[-1]["outputs"].append("vertex{}".format(i+1))
                template.append(vertex)
            vertex = {"outputs":[],"type":"output","attr":{},"uid":"vertex2"}
            vertex["uid"] = "vertex{}".format(math.ceil(int(module["deepth"]))+1)
            template[-1]["outputs"].append("vertex{}".format(math.ceil(int(module["deepth"]))+1))
            template.append(vertex)
            graph = self.gGraph(template)
            graph['type'] = module['type']
            graph['channels'] = module['channels']
            self.level2.append(graph)
     
    def gGraph(self,skelen):
        graph = {"lineList":[],"nodeList":[]}
        for vertex in skelen:
            obj = {}
            obj['attrs'] = vertex['attr']
            TYPE = vertex['type']
            obj['type'] = TYPE
            obj['id'] = vertex['uid']
            obj['nodeName'] = TYPE
            obj['typeName'] = TYPE
            obj['log_bg_color'] = "rgba(250, 205, 81, 0.2)"
            graph['nodeList'].append(obj)

            for output in vertex["outputs"]:
                line = {}
                line['Remark'] =''
                line['from'] = vertex['uid']
                line['to'] = output
                line['label'] = "连线名称"
                line['id'] = "{}-{}".format(vertex['uid'],output) 
                graph['lineList'].append(line)
        return graph

    def initPopulation(self):
        self.produceOrigin(self.moduleList)
        originChild = model(self.level1,self.level2)
        originChild.assemble()
        acc,loss = self.train(originChild)
        
        self.population.append({"child":originChild,"acc":acc,"loss":loss})


    def ga(self):
        parent = self.getNet()["child"]
        child = model(parent.level1,parent.level2)
        child.vary()
        child.assemble()
        acc,loss = self.train(child)
        self.population.append({"child":child,"acc":acc,"loss":loss})
    
    def getNet(self):
        '''亲代选择'''
        pair = []
        for _ in range(2):
            '''下标'''
            sample = random.sample(list(range(len(self.population))), 1)
            pair.append(sample[0])
        better_net,worse_net = [pair[0],pair[1]] if self.population[pair[0]]["acc"] >= self.population[pair[1]]["acc"] else [pair[1],pair[0]]
        res = self.population[better_net]
        '''种群规模达到上限，剔除性能较差的模型'''
        if len(self.population) == self.limit:
            self.population.pop(worse_net)
        return res
    
    
    def train(self,graph):
        
        modules = [m['type'] for m in self.moduleList]
        for v in self.skelen["nodeList"]:
            if v["type"] in modules:
                index = modules.index(v["type"])
                vertex = graph.LEVEL2_ENTITY[index]

                v["nodeList"] = vertex["nodeList"]
                v['lineList'] = vertex["lineList"]
        
        basepath = "Prun/automl/{}".format(self.account)
        os.makedirs(basepath)
        # TODO
        skelen = json.loads(json.dumps(self.skelen))
        self.clearSequence(skelen)
        # **************
        # 写入结构文件
        with open("{}/model.json".format(basepath),"w") as f:
            json.dump(skelen, f)
        modelc = createModel("{}/model.json".format(basepath))
        trainer= Trainer(model = modelc,epoch = self.epoch)
        
        # loss = random.random()
        # acc = random.random()
        acc,loss,tacc = trainer.train()
        
        
        with open("{}/performance.json".format(basepath),"w") as f:
            json.dump({"acc":acc,"loss":loss}, f)
        os.mkdir("{}/parameter".format(basepath))
        # trainer.save("{}/parameter/model.pth".format(basepath))
        torch.save(modelc.state_dict(),"{}/parameter/model.pth".format(basepath))
        

        # with open("p1.json","w") as f:
        #     json.dump(self.skelen, f)
        # modelc = createModel("p1.json")
        # x = Variable(torch.randn(10, 3, 32, 32))
        # torch.onnx.export(modelc, x, 
        #     "test{}.onnx".format(self.account),
        #     export_params=True,
        #     verbose=True)
        # modelc(x)
        self.account += 1
        return (acc,loss)
    
    def clearSequence(self,g):
        for vertex in g["nodeList"]:
            if vertex["type"].startswith("auto"):
                # 模块内节点数
                vn = len(vertex["nodeList"])
                if vn == 3:
                    continue
                # 记录straight
                straight = []
                vs = []
                for v in vertex["nodeList"]:
                    if v['type'] == 'level1[3]':
                        straight.append(v['id'])
                    vs.append(v['id'])
                # 模块内至少保留一个节点
                if len(straight) == (vn-2):
                    straight.pop()
                # 序列重构
                index = 0
                while index < len(vs):
                    if vs[index] in straight:
                        vs.pop(index)
                    else:
                        index += 1
                vertex['lineList'] = []
                for index in range(1,len(vs)):
                    line = {'Remark': '', 'from': 'vertex0', 'to': 'vertex1', 'label': '连线名称', 'id': 'vertex0-vertex1'}
                    line['from'] = vs[index-1]
                    line['to'] = vs[index]
                    line['id'] = "{}-{}".format(vs[index-1],vs[index])
                    vertex["lineList"].append(line)
                
                for index in range(vn-1,-1,-1):
                    if vertex["nodeList"][index]['id'] in straight:
                        vertex["nodeList"].pop(index)
                
                
    # def process(g):
    
        
# holderPlace = None
# skelen = None
# with open("autoModule.json","r") as f:
#     holderPlace = json.load(f)

# with open("graph.json","r") as f:
#     skelen = json.load(f)

# f = Factory(LEVEL_0, LEVEL_1, skelen, holderPlace)
# f.initPopulation()

# for i in range(300):
#     f.ga()


# with open("graph.json",'w') as f:
#     json.dump(testGraph, f)
# m = model(LEVEL_1,LEVEL_2)
# m.vary()