import numpy as np
import json
import random
import traceback
import time
import os

from .validate.validator import *
from .compile import compile
from .train import Trainer

'''
产生突变：
1.删除卷积层 (影响特征图空间分辨率,输出维度)(修改下层卷积层，修改相关skip)
2.增加卷积层（3*3,通道数与上层保持一致,padding随机设置(SAME/VALID),随机增加 bn/relu (0/1个)，修改相关skip，pass）
3.继续训练
4.增加skip (1*1卷积匹配维度，sampling匹配空间分辨率，pass)
5.删除skip (直接删除，检查后续add操作，pass)
6.修改滤波器大小 (影响特征图空间分辨率)(滤波器大小为奇数，修改相关skip，pass)
7.卷积层通道数(影响输出维度)（1/2~2，修改相关skip）
8.增加maxpool/avgpool (影响特征图空间分辨率)(修改相关skip，pass)
9.删除maxpool/avgpool (影响特征图空间分辨率)(修改相关skip，pass)
'''
class mutationOp:
    def __init__(self,orc_graph=None,img_shape=None,deep=None,predict=None,config=None,epoch=100,limit = 100):
        '''
            pupulation:种群
            limit:种群大小
            choices:突变方法
            p:突变概率
            epoch:遗传算法执行次数
            deep:深度限制
            predict:预测类别
        '''
        '''
        {"net":{},"acc":...}
        '''
        self._epoch = 0
        self._predict = predict
        self._deep = deep
        self._limit = limit
        self._img_shape = img_shape
        self._tol_epoch = epoch
        self._config = config
        self._population = [orc_graph]
        all_method = self.__dir__()
        self._choices = self._filter(all_method)
        self._validator = Validator()
        method_num = len(self._choices)
        self._p = [1/method_num for _ in range(method_num)]
        # 添加规则
        self._validator.add_rule(ValidateFixLayer()).add_rule(ValidateDepth()).add_rule(ValidateLayerGap())
    
    def ga(self):
        self._epoch += 1
        '''亲代选择'''
        net = self._getNet()
        '''变异'''
        
        net = self._generate_child(net)
        if len(list(net.keys())) > 0:
            net_ = json.loads(json.dumps(net))
            net_ = self._complete_net(net_)
        
            '''评估'''
            acc = 0
            try:
                acc = self._evalute(net_)
                print(acc)
                self._population.append({"net":net,"acc":acc})
            except Exception as e:
                print(e)
                acc = 0
            '''加入种群'''
        
            # self._population.append({"net":net,"acc":acc})
        
    def _complete_net(self,net):
        joint,channels = None,None
        try:
            joint,channels = self._get_exit(net)
        except Exception:
            channels = self._img_shape[0]
        net_ = json.loads(json.dumps(net))
        net_[joint]["outputs"].append(self._add_exit(joint, channels, net_))
        return net_
        
    def get_population(self):
        self._population.sort(key=lambda x:x["acc"],reverse=True)
        return self._population
    
    def _evalute(self,net=None):
        basepath = "log/{}".format(self._epoch)
        os.makedirs(basepath)
        # 写入结构文件
        with open("{}/model.json".format(basepath),"w") as f:
            json.dump(net, f)
        model = compile(basepath)
        trainer= Trainer(model)
        print(trainer)
        acc,loss = trainer.train()
        with open("{}/performance.json".format(basepath),"w") as f:
            json.dump({"acc":acc,"loss":loss}, f)

        return acc
    
    def _getNet(self):
        '''亲代选择'''
        pair = []
        for _ in range(2):
            '''下标'''
            sample = random.sample(list(range(len(self._population))), 1)
            pair.append(sample[0])
        better_net,worse_net = [pair[0],pair[1]] if self._population[pair[0]]["acc"] >= self._population[pair[1]]["acc"] else [pair[1],pair[0]]
        res = self._population[better_net]["net"]
        '''种群规模达到上限，剔除性能较差的模型'''
        if len(self._population) == self._limit:
            self._population.pop(worse_net)
        
        return res
    
    def _generate_child(self,net):
        '''变异'''
        
        # choice = "add_pool"
        
        while True:
            finih_tag = True
            net_copy = json.loads(json.dumps(net))
            try:
                choice = np.random.choice(self._choices,p=self._p)
                
                # choice = "drop_conv"
                print(choice)
                finih_tag = self.__getattribute__(choice)(net_copy)
                finih_tag = finih_tag & self._validate(net_copy)
            except Exception as e:
                traceback.print_exc()
                finih_tag = False
            if finih_tag:
                break
        self._modify_skip(net_copy)
        return net_copy
            
    def _filter(self,all_method):
        '''过滤非突变操作'''
        methods = ["ga","get_population"]
        def mutationOpFilter(x):
            if x.startswith("_") or x in methods :
                return False
            else:
                return True
        res = list(filter(mutationOpFilter, all_method))
        return res
        
    def _get_related_skip(self,net):
        '''获取相关skip'''
        '''topo:主线路节点排序'''
        
        pass
        
    def _random_channel(self, x):
        '''随机通道数'''
        res = np.random.randint(int(x/2),2*x)
        return res

    def _random_filterSize(self, x):
        '''随机滤波器大小,必须为奇数'''
        res = np.random.randint(int(x/2),2*x)
        res = res if res%2 == 1 else res + 1
        return res
    
    def _has_skip(self, net):
        '''
            是否有skip
            返回skip列表,skip上节点
        '''
        def cross_finder(vertex,path):
            path.append(vertex)
            if len(net[vertex]["inputs"]) == 1 and len(net[vertex]["outputs"]) ==1:
                cross_finder(net[vertex]["outputs"][0], path)
            elif len(net[vertex]["outputs"]) >1:
                path.clear()
                
        skip_list = []
        for i in net.keys():
            '''多个出口'''
            if len(net[i]["outputs"]) > 1:
                for j in net[i]["outputs"]:
                    path = [i]
                    cross_finder(j, path)
                    if len(path) != 0:
                        skip_list.append(path)
        res = []
        vertexs = set()
        for skip in skip_list:
            if len(skip) == 4 and net[skip[1]]["type"].startswith("conv") and net[skip[2]]["type"].startswith("op_sampling"):
                res.append(skip)
                vertexs.add(skip[1])
                vertexs.add(skip[2])
        
        return (res,vertexs)
                        
    def _has_special_type(self,net,type):
        '''
            是否有指定类型网络层
            返回网络层列表
        '''
        specify_list = []
        for i in net.keys():
            if net[i]["type"].startswith(type):
               specify_list.append(i)
        return specify_list
            
    def modify_channel(self,net,vertexId=None,channel=None):
        '''修改通道数'''
        conv_list = self._has_special_type(net,"conv")
        
        res,skip_vertex_list = self._has_skip(net)
        
        main_flow = [] # 可以选择的点
        for vertex in conv_list:
            if (not vertex in skip_vertex_list):
                main_flow.append(vertex)
        
        if len(main_flow) == 0:
            return False
        else:
            target_conv = vertexId or np.random.choice(main_flow)
            out_channels = channel or self._random_channel(net[target_conv]["attr"]["out_channels"])
            net[target_conv]["attr"]["out_channels"] = out_channels
            if len(net[target_conv]["outputs"]) == 0:
                return True
            next_vertex = net[target_conv]["outputs"][0]
            while True:
                if net[next_vertex]["type"].startswith("bn"):
                    net[next_vertex]["attr"]["num_features"] = out_channels
                elif net[next_vertex]["type"].startswith("conv"):
                    net[next_vertex]["attr"]["in_channels"] = out_channels
                    break
                if len(net[next_vertex]["outputs"]) == 0:
                    break
                next_vertex = net[next_vertex]["outputs"][0]
        self._modify_skip(net)
        return True
        
    def modify_filter(self,net):
        '''修改滤波器大小'''
        conv_list = self._has_special_type(net,"conv")

        res,skip_vertex_list = self._has_skip(net)
        
        main_flow = [] # 可以选择的点
        for vertex in conv_list:
            if (not vertex in skip_vertex_list):
                main_flow.append(vertex)
        
        if len(main_flow) == 0:
            return False
        else:
            target_conv = np.random.choice(main_flow)
            kernel_size = self._random_filterSize(net[target_conv]["attr"]["kernel_size"])
            net[target_conv]["attr"]["kernel_size"] = kernel_size
        self._modify_skip(net)
        return True
    
    def drop_conv(self,net):
        '''丢弃卷积层'''
        
        # 遇见op_add或者分叉点不继续删
        conv_list = self._has_special_type(net,"conv")
            
        _,skip_vertex_list = self._has_skip(net)
        # 可以选择的点,在主路上，不能是分支起点
        main_conv_vertexs = [] 
        for vertex in conv_list:
            if (not vertex in skip_vertex_list) and (len(net[vertex]["outputs"]) == 1):
                main_conv_vertexs.append(vertex)
        
        # 主线上所有点
        main_flow = [] 
        
        G = {}
        for vertex in net:
            G[vertex] = net[vertex]["outputs"]
        topo_list = self._topological_sort(G)
        
        
        for vertex in topo_list:
            if (not vertex in skip_vertex_list):
                main_flow.append(vertex)

        drop_conv = None

        if len(main_conv_vertexs) <= 1:
            print("无节点可删")
            return False
        
        else:
            # for layer in net:
            #     print(net[layer])
            # 随计选择conv
            drop_conv = np.random.choice(main_conv_vertexs)
            # input_vertex drop的输入节点
            input_vertex = None
            if len(net[drop_conv]["inputs"]) > 0:
                input_vertex = net[drop_conv]["inputs"][0]
            channel = net[drop_conv]["attr"]["in_channels"]
            # 查找drop_conv的下标
            vertex_index = main_flow.index(drop_conv)
            
            drop_tag = True # 丢弃tag，true时del网络层
            end_vertex = None # input_vertex后续节点
            # print("main_flow",main_flow)
            for index in range(vertex_index+1,len(main_flow)):
                layer_id = main_flow[index]
                # 遇见卷积
                if net[layer_id]["type"].startswith("conv"):
                    # 修改通道数
                    net[layer_id]["attr"]["in_channels"] = channel
                    # drop_tag true时拼接输入节点和该节点
                    if drop_tag:
                        if input_vertex:
                            net[layer_id]["inputs"] = [input_vertex]
                        else:
                            net[layer_id]["inputs"] = []
                    if not end_vertex:
                        end_vertex = layer_id
                    break
                # 遇见skip起始或者skip终止
                elif net[layer_id]["type"] == "op_add" or len(net[layer_id]["outputs"])>1:
                    if len(net[layer_id]["outputs"]) > 1 and (not input_vertex):
                        return False
                    if drop_tag:
                        for i in range(len(net[layer_id]["inputs"])):
                            try:
                                if net[layer_id]["inputs"][i] == main_flow[index-1]:
                                    if input_vertex:
                                        net[layer_id]["inputs"][i] = input_vertex
                                    else:
                                        del net[layer_id]["inputs"][i]
                                break
                            except Exception as e:
                                traceback.print_exc()
                    drop_tag = False
                    if not end_vertex:
                        end_vertex = layer_id
                # 遇见bn
                elif net[layer_id]["type"].startswith("bn"):
                    if drop_tag:
                        del net[layer_id]
                    else:
                        net[layer_id]["attr"]["num_features"] = channel
                else:
                    if drop_tag:
                        del net[layer_id]
            
        
        if input_vertex:
            if end_vertex:
                net[input_vertex]["outputs"] = [end_vertex]
            else:
                net[input_vertex]["outputs"] = []
        del net[drop_conv]
        self._modify_skip(net)
        
        return True
        
    def _has_next(self,net,node,type):
        if net[node]["type"].startswith(type):
            return node
        else:
            if len(net[node]["outputs"]) == 0:
                return 0
            else:
                return self._has_next(net,net[node]["outputs"][0] ,type)
            
    def _get_uid(self,uid):
        return "epoch"+str(self._epoch) + "_" + uid
    
    def add_conv(self,net):
        '''增加卷积层'''
        # step1:选择插入位置,point_choice,dir_choice,bn_choice
        # step2:生成模块
        # step3:插入，dir_choice为1时需要考虑后续节点为op_add
        keys = list(net.keys())
        uid = len(keys) + 1
        point_choice = None
        
        res,skip_vertex_list = self._has_skip(net)
        
        main_flow = [] # 可以选择的点
        for vertex in keys:
            if (not vertex in skip_vertex_list):
                main_flow.append(vertex)
        
        while True:
            point_choice = np.random.choice(main_flow)
            if net[point_choice]["type"] != "op_add":
                break
        dir_choice = np.random.choice([0,1]) # 0前向插入，1后向插入
        bn_choice = np.random.choice([0,1]) # 0不加rn，1加入rn
        # 获取通道数
        def get_channel(point):
            if net[point]["type"] == "conv2d":
                return net[point]["attr"]["out_channels"]
            elif len(net[point]["inputs"]) == 0:
                return self._img_shape[0]
            else:
                return get_channel(net[point]["inputs"][0])
        # 局部模块
        def g_partial(intputs,outputs,channels,bn):
            part = {}
            conv = {}
            conv["attr"] = {"padding":0,"bias":True,"stride":1,"in_channels":channels,"out_channels":channels,"kernel_size":3}
            conv["inputs"] = intputs
            conv["type"] = "conv2d"
            conv["moduleId"] = "/conv2d"
            conv["uid"] = self._get_uid("layer" + str(uid))
            if bn == 0:
                conv["outputs"] = outputs
                part["conv2d"] = conv
            else:
                conv["outputs"] = [self._get_uid("layer" + str(uid+1))]
                bn = {}
                bn["attr"] = {"num_features": channels}
                bn["inputs"] = [self._get_uid("layer" + str(uid))]
                bn["type"] = "bn2d"
                bn["moduleId"] = "/bn2d"
                bn["uid"] = self._get_uid("layer" + str(uid + 1))
                bn["outputs"] = [self._get_uid("layer" + str(uid+2))]
                relu = {}
                relu["attr"] = {}
                relu["inputs"] = [self._get_uid("layer" + str(uid+1))]
                relu["type"] = "relu"
                relu["moduleId"] = "/relu"
                relu["uid"] = self._get_uid("layer" + str(uid + 2))
                relu["outputs"] = outputs
                part["conv2d"] = conv
                part["bn2d"] = bn
                part["relu"] = relu
            return part
        
        inputs,outputs,channel = None,None,None
        # 所选节点前方插入
        if dir_choice == 0:
            inputs = net[point_choice]["inputs"] # 新卷积节点输入
            outputs = [point_choice] 
            # 检索channel
            if len(net[point_choice]["inputs"]) == 0:
                channel = self._img_shape[0]
            else:
                channel = get_channel(net[point_choice]["inputs"][0])
            # 修改输入口outputs
            for input in net[point_choice]["inputs"]:
                index = net[input]["outputs"].index(point_choice)
                net[input]["outputs"] = json.loads(json.dumps(net[input]["outputs"]))
                net[input]["outputs"][index] = self._get_uid("layer" + str(uid))
            net[point_choice]["inputs"] = [self._get_uid("layer" + str(uid)) if bn_choice == 0 else self._get_uid("layer"+str(uid+2))]
        # 所选节点后方插入
        else:
            inputs = [point_choice] # 新卷积节点输入
            outputs = net[point_choice]["outputs"]
            channel = get_channel(point_choice) # 新卷积节点通道数
            
            for output in net[point_choice]["outputs"]:
                index = net[output]["inputs"].index(point_choice)
                net[output]["inputs"] = json.loads(json.dumps(net[output]["inputs"]))
                net[output]["inputs"][index] = self._get_uid("layer" + str(uid)) if bn_choice == 0 else self._get_uid("layer" + str(uid + 2))
            
            net[point_choice]["outputs"] = [self._get_uid("layer" + str(uid))]
            
        part = g_partial(inputs,outputs,channel,bn_choice)
        # 局部模块加入整体
        for i in part:
            uid = part[i]["uid"]
            net[uid] = part[i]
        self._modify_skip(net)
        return True
        
    def _add_exit(self,joint,channels,net):
        '''添加output'''
        keys = list(net.keys())
        uid = len(keys) + 1
        
        adaptiveavgpool2d = {}
        adaptiveavgpool2d["uid"] = "exit-"+"layer" + str(uid)
        adaptiveavgpool2d["attr"] = {}
        adaptiveavgpool2d["inputs"] = [joint]
        adaptiveavgpool2d["type"] = "adaptiveavgpool2d"
        adaptiveavgpool2d["moduleId"] = "/adaptiveavgpool2d"
        adaptiveavgpool2d["outputs"] = ["exit-" + "layer" + str(uid+1)]
        net["exit-" + "layer" + str(uid)] = adaptiveavgpool2d
        
        view = {}
        view["uid"] = "exit-" + "layer" + str(uid+1)
        view["attr"] = {}
        view["inputs"] = ["exit-" + "layer" + str(uid)]
        view["type"] = "op_view"
        view["moduleId"] = "/view"
        view["outputs"] = ["exit-" + "layer" + str(uid+2)]
        net["exit-" + "layer" + str(uid+1)] = view
        
        linear = {}
        linear["uid"] = "exit-" + "layer" + str(uid+2)
        linear["attr"] = {"in_features":channels,"out_features":self._predict,"bias":True}
        linear["inputs"] = ["exit-" + "layer" + str(uid+1)]
        linear["type"] = "linear"
        linear["moduleId"] = "/linear"
        linear["outputs"] = []
        net["exit-" + "layer" + str(uid+2)] = linear
        return "exit-" + "layer" + str(uid)
        
    def _replace(self,vertex_list, source, target):
        '''替换节点'''
        for index in range(len(vertex_list)):
            if vertex_list[index] == source:
                vertex_list[index] = target
                break
    
    def _modify_skip(self,net):
        '''修改skip'''
        # step1:获取所有skip
        res,skip_vertex_list = self._has_skip(net)
        # step2:主路节点拓扑排序
        G = {}
        for vertex in net:
            G[vertex] = net[vertex]["outputs"]
        topo_list = self._topological_sort(G)
        
        main_flow = [] # 可以选择的点
        for vertex in topo_list:
            if (not vertex in skip_vertex_list):
                main_flow.append(vertex)
        # step2:修改所有skip
        for skip in res:
            start_index = main_flow.index(skip[0])
            end_index = main_flow.index(skip[3])
            
            diff = 0 # 记录减小尺寸
            out_channels = 0 # 记录通道
            in_channels = 0
            for i in range(start_index+1,end_index):
                if net[main_flow[i]]["type"].startswith("conv"):
                    diff += net[main_flow[i]]["attr"]["kernel_size"] - 1 - 2*net[main_flow[i]]["attr"]["padding"]
            
            for i in range(end_index-1,start_index,-1):
                if net[main_flow[i]]["type"].startswith("conv"):
                    out_channels = net[main_flow[i]]["attr"]["out_channels"]
                    break
                    
            for i in range(start_index,-1,-1):
                if net[main_flow[i]]["type"].startswith("conv"):
                    in_channels = net[main_flow[i]]["attr"]["out_channels"]
                    break
                    
            if in_channels == 0:
                in_channels = self._img_shape[0]
            
            if out_channels == 0:
                out_channels = in_channels
            
            net[skip[1]]["attr"]["in_channels"] = in_channels
            net[skip[1]]["attr"]["out_channels"] = out_channels
            net[skip[2]]["attr"]["diff"] = diff
        
    def _get_exit(self,net):
        output_channel = self._img_shape[0]
        start_point = None
        # 起点
        for vertex in net.keys():
            if len(net[vertex]["inputs"]) == 0:
                start_point = vertex
        vertex = start_point
        while True:
            # 未到终点
            if len(net[vertex]["outputs"]) != 0:
                # 卷积
                if net[vertex]["type"].startswith("conv"):
                    output_channel = net[vertex]["attr"]["out_channels"]
                    vertex = net[vertex]["outputs"][0]
                # 非卷积
                else:
                    vertex = net[vertex]["outputs"][0]
            # 到终点
            else:
                # 卷积结尾
                if net[vertex]["type"].startswith("conv"):
                    output_channel = net[vertex]["attr"]["out_channels"]
                break

        return (vertex,output_channel)
    
    def add_skip(self,net):
        '''增加skip'''
        _,skip_vertex_list = self._has_skip(net)
        keys = list(net.keys())
        G = {}
        for vertex in net:
            G[vertex] = net[vertex]["outputs"]
        topo_list = self._topological_sort(G)
        uid = len(keys) + 1
        start_choice = None # 起始点
        end_choice = None # 终止点
        
        choice_able = [] # 可以选择的点
        for vertex in topo_list:
            if net[vertex]["type"] != "op_add" and (not vertex in skip_vertex_list):
                choice_able.append(vertex)
        
        start_choice = np.random.choice(list(range(len(choice_able)-1)))
        end_choice = np.random.choice(list(range(start_choice+1,len(choice_able))))
        
        diff = 0 # 记录减小尺寸
        out_channels = 0 # 记录通道
        in_channels = 0
        for i in range(start_choice+1,end_choice):
            if net[choice_able[i]]["type"].startswith("conv"):
                diff += net[choice_able[i]]["attr"]["kernel_size"] - 1 - 2*net[choice_able[i]]["attr"]["padding"]
        
        for i in range(end_choice-1,start_choice,-1):
            if net[choice_able[i]]["type"].startswith("conv"):
                out_channels = net[choice_able[i]]["attr"]["out_channels"]
                break
                
        for i in range(start_choice,-1,-1):
            if net[choice_able[i]]["type"].startswith("conv"):
                in_channels = net[choice_able[i]]["attr"]["out_channels"]
                break
                
        if in_channels == 0:
            in_channels = self._img_shape[0]
        
        if out_channels == 0:
            out_channels = in_channels
        
        # 生成skip，不包括起始点和终止点
        def g_skip(in_channels,out_channels,diff):
            conv = {}
            conv["attr"] = {"padding":0,"bias":True,"stride":1,"in_channels":in_channels,"out_channels":out_channels,"kernel_size":1}
            conv["inputs"] = []
            conv["type"] = "conv2d"
            conv["moduleId"] = "/conv2d"
            conv["uid"] = self._get_uid("layer" + str(uid))
            conv["outputs"] = [self._get_uid("layer" + str(uid+1))]
            
            op_sampling = {}
            op_sampling["attr"] = {"diff":diff}
            op_sampling["inputs"] = [conv["uid"]]
            op_sampling["type"] = "op_sampling"
            op_sampling["moduleId"] = "/op_sampling"
            op_sampling["uid"] = self._get_uid("layer" + str(uid+1))
            op_sampling["outputs"] = [self._get_uid("layer" + str(uid+2))]
            
            op_add = {}
            op_add["attr"] = {}
            op_add["inputs"] = [op_sampling["uid"]]
            op_add["type"] = "op_add"
            op_add["moduleId"] = "/op_add"
            op_add["uid"] = self._get_uid("layer" + str(uid+2))
            op_add["outputs"] = []
            
            return (conv,op_sampling,op_add)
            
        conv,op_sampling,op_add = g_skip(in_channels,out_channels,diff)
        
        start_vertex = choice_able[start_choice]
        end_vertex = choice_able[end_choice]
        # 处理入口
        net[start_vertex]["outputs"].append(conv["uid"])
        conv["inputs"].append(start_vertex)
        # 处理出口
        # 插入op_add
        end_pre = net[end_vertex]["inputs"][0]
        for index in range(len(net[end_pre]["outputs"])):
            if net[end_pre]["outputs"][index] == end_vertex:
                net[end_pre]["outputs"][index] = op_add["uid"]
        net[end_vertex]["inputs"] = [op_add["uid"]]
        
        op_add["outputs"].append(end_vertex)
        
        op_add["inputs"].append(end_pre)
        
        net[conv["uid"]] = conv
        net[op_sampling["uid"]] = op_sampling
        net[op_add["uid"]] = op_add
        return True
    
    def drop_skip(self,net):
        '''丢弃skip'''
        res,skip_vertex_list = self._has_skip(net)
        if len(res) == 0:
            return False
        
        choice = np.random.choice(list(range(len(res))))
        skip_choice = res[choice]
        
        start_point = skip_choice[0]
        end_point = skip_choice[3]
        # 处理入口节点
        try:
            for vertex_index in range(len(net[start_point]["outputs"])):
                if net[start_point]["outputs"][vertex_index] == skip_choice[1]:
                    del net[start_point]["outputs"][vertex_index]
                    break
        except Exception:
            print(net[start_point]["outputs"][vertex_index])
            print(skip_choice)
        # op_add后节点
        main_trail_end_point = None
        if len(net[end_point]["outputs"]) > 0:
            main_trail_end_point = net[end_point]["outputs"][0]
        main_pre_end_point = None
        # 查找op_add前节点
        for vertex_index in range(len(net[end_point]["inputs"])):
            if net[end_point]["inputs"][vertex_index] != skip_choice[2]:
                main_pre_end_point = net[end_point]["inputs"][vertex_index]
                break
        # 替换op_add后节点inputs
        if main_trail_end_point:
            for vertex_index in range(len(net[main_trail_end_point]["inputs"])):
                if net[main_trail_end_point]["inputs"][vertex_index] == skip_choice[3]:
                    net[main_trail_end_point]["inputs"][vertex_index] = main_pre_end_point
                    break
        # 替换op_add前节点outputs
        for vertex_index in range(len(net[main_pre_end_point]["outputs"])):
            if net[main_pre_end_point]["outputs"][vertex_index] == skip_choice[3]:
                if main_trail_end_point:
                    net[main_pre_end_point]["outputs"][vertex_index] = main_trail_end_point
                else:
                    del net[main_pre_end_point]["outputs"][vertex_index]
                break
        
        for vertex in skip_choice[1:]:
            del net[vertex]
        
        return True
    
    def _add_pool(self,net):
        '''增加 maxpool/avgpool '''
        keys = list(net.keys())
        uid = len(keys)
        avgpool2d = {}
        avgpool2d["uid"] = self._get_uid(str(uid+1))
        avgpool2d["attr"] = {"stride":2,"kernel_size":2,"padding":0}
        avgpool2d["inputs"] = []
        avgpool2d["type"] = "avgpool2d"
        avgpool2d["moduleId"] = "/avgpool2d"
        avgpool2d["outputs"] = []
        point_choice = None
        while True:
            point_choice = np.random.choice(keys)
            if net[point_choice]["type"] != "op_add":
                break
        avgpool2d["inputs"] = [point_choice]
        
        if len(net[point_choice]["outputs"]) == 0:
            net[point_choice]["outputs"] = [avgpool2d["uid"]]
            
        else:
            avgpool2d["outputs"] = net[point_choice]["outputs"]
            net[point_choice]["outputs"] = [avgpool2d["uid"]]
            net[avgpool2d["outputs"][0]]["inputs"] = [avgpool2d["uid"]]

        net[avgpool2d["uid"]] = avgpool2d
        return True

    def _drop_pool(self,net):
        '''删除 maxpool/avgpool'''
        pool_list = self._has_special_type(net, "avgpool")
        if len(pool_list) == 0:
            return False
        
        point_choice = np.random.choice(pool_list)
        pre,tail = None,None
        if len(net[point_choice]["inputs"])>0:
            pre = net[point_choice]["inputs"][0]
        if len(net[point_choice]["outputs"]) > 0:
            tail = net[point_choice]["outputs"][0]

        if pre:
            net[pre]["outputs"] = [tail] if tail else []
        if tail:
            net[tail]["inputs"] = [pre] if pre else []
        
        del net[point_choice]
        return True

    def _topological_sort(self,G):
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
        ''' 创建入度字典 '''
        # print(G)
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
    
    def _validate(self,net):
 
        
        # .add_rule(ValidateDepth)
        _,skip_vertex_list = self._has_skip(net)
        # 验证
        res = self._validator.execute(net, self._config, skip_vertex_list)
        return res
        
        

def fetch_init_info(basepath):
    graph = None
    config = None
    with open("{}/store/base.json".format(basepath),"r") as f:
        graph = json.load(f)
    net = {"net":graph,"acc":0}
    with open("{}/store/config.json".format(basepath), "r") as f:
        config = json.load(f)
    obj = mutationOp(net, [3,32,32], 100, 10, config, 100)
    res = obj._validate(graph)
    
    return obj

# obj = fetch_init_info(".")

    



# for i in range(10):
#     obj.ga()
# size = len(obj._population)

# with open("model.json","w") as f:
#     choice = size-1
#     net_ = obj._population[-1]["net"]
#     net_ = obj._complete_net(net_)
#     json.dump(net_, f)
# compile(".")

