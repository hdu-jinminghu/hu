import torch
import torch.nn as nn
import torch.nn.functional as F #加载nn中的功能函数
import torch.optim as optim #加载优化器有关包
import torch.utils.data as Data
from torchvision import datasets,transforms #加载计算机视觉有关包
from torch.autograd import Variable
import json
import numpy as np
import time
# from tensorboardX import SummaryWriter
import torchvision
import os
# import pack
from itertools import groupby
import functools
import cv2
import shutil
import scipy
import math
from scipy.interpolate import interp2d
import tables
from PIL import Image
import matplotlib.pyplot as plt
from .pre_process import kernel_size,model_structure
# import utils.pre_process as pre_process
from ptflops import get_model_complexity_info
import shutil
from torch.nn.parameter import Parameter
import re
import gc
from shutil import move
from Prun.backend.automl.ga.ga import mutationOp
SEPARATOR = '*'
# 保存模型及参数,需要注销钩子函数
def graph(model=None,args=None,path=".",name="",trueIndex = "model_0",virtualIndex=0,tag=True):
    tPath = path
    if tag:
        tPath = path + "/" + "model_0"
    if not os.path.exists(tPath):
            os.makedirs(tPath)
    # kernel_size(model, tPath,name)
    # model_structure(model, args, tPath,name)
#  计算敏感度
def sensitity(weight, grad):
    s = weight * grad
    return torch.sum(s,dim=[1,2])

# 计算平均秩,返回各个通道的秩
def saturation(output):
    a = output.shape[0]
    b = output.shape[1]
    c = torch.tensor([torch.matrix_rank(output[i,j,:,:]).item() for i in range(a) for j in range(b)])
    d = output.shape[2]
    total = torch.tensor(0.)
    feature_result = torch.tensor(0.)
    c = c.view(a, -1).float()
    c = c.sum(0)
    feature_result = feature_result * total + c
    total = total + a
    feature_result = feature_result / total
    return feature_result
#  剪枝起始卷积核
# 替换参数会导致反向传播梯度矩阵大小不匹配
'''
*target_id:目标层
*prun_list:剪枝通道
*path:剪枝参数储存路径
'''
def prunConv1(model = None, target_id = None, prun_list = None,path="."):
    if target_id == "None":
        return
    id_ = target_id.split(SEPARATOR)
    module = model
    trueid = ""
    for id in id_[1:-1]:
        trueid = trueid+SEPARATOR+id
        module = module._modules[trueid]
    # 更换删除卷积核
    trueid = trueid+SEPARATOR+id_[-1]
    # manage_module = module._modules[id_[-1]]
    manage_module = module._modules[trueid]
    kernel_total = manage_module.weight.shape[0]
    preserve = set(range(kernel_total)) - set(prun_list)
    preserve_weight = manage_module.weight[list(preserve)].clone()
    preserve_bias = None
    daop_bias = None
    if manage_module.bias != None:
        preserve_bias = manage_module.bias[list(preserve)].clone()
        daop_bias = manage_module.bias[list(prun_list)].clone()
    new_conv = None
    # param = {}
    # param["weight"] = manage_module.weight[list(prun_list)].cpu().data
    # if daop_bias:
    #     param["bias"] = daop_bias.cpu().data
    # ti = target_id.replace(".", "-")
    # np.savez("{}/channel_conv1_{}.npz".format(path,ti),**param)
    if isinstance(manage_module,torch.nn.Conv2d):
        new_conv = torch.nn.Conv2d(in_channels=manage_module.in_channels, 
                        out_channels=len(preserve),
                        kernel_size=manage_module.kernel_size,
                        stride=manage_module.stride,
                        padding=manage_module.padding,
                        bias=True if manage_module.bias != None else False)
    elif isinstance(manage_module,torch.nn.Conv1d):
        new_conv = torch.nn.Conv1d(in_channels=manage_module.in_channels, 
                        out_channels=len(preserve),
                        kernel_size=manage_module.kernel_size,
                        stride=manage_module.stride,
                        padding=manage_module.padding,
                        bias=True if manage_module.bias != None else False)

    new_conv.weight = Parameter(preserve_weight)
    if manage_module.bias != None:
        new_conv.bias = Parameter(preserve_bias)
    new_conv.uid = trueid
    # module._modules[id_[-1]] = new_conv
    module._modules[trueid] = new_conv
    return manage_module.out_channels
    
# 剪枝归一化层
def prunBn(model = None, target_id = None, prun_list = None,path="."):
    if target_id == "None":
        return
    id_ = target_id.split(SEPARATOR)
    module = model
    trueid = ""
    for id in id_[1:-1]:
        trueid = trueid+SEPARATOR+id
        module = module._modules[trueid]
        
    trueid = trueid+SEPARATOR+id_[-1]
    # tackle_module = module._modules[id_[-1]]
    tackle_module = module._modules[trueid]
    
    
    kernel_total = tackle_module.weight.shape[0]
    preserve = set(range(kernel_total)) - set(prun_list)
    new_bn = None
    if isinstance(tackle_module, torch.nn.BatchNorm2d):
        new_bn = torch.nn.BatchNorm2d(num_features=len(preserve))
    elif isinstance(tackle_module, torch.nn.BatchNorm1d):
        new_bn = torch.nn.BatchNorm1d(num_features=len(preserve))
    
    manage_bn_module_weight = tackle_module.weight
    manage_bn_module_bias = tackle_module.bias
    
    
    new_bn.weight = Parameter(manage_bn_module_weight[list(preserve)].clone())
    # if tackle_module.bias:
    new_bn.bias = Parameter(manage_bn_module_bias[list(preserve)].clone())
    new_bn.running_mean = tackle_module.running_mean[list(preserve)].clone()
    new_bn.running_var = tackle_module.running_var[list(preserve)].clone()
    new_bn.uid = trueid
    # module._modules[id_[-1]] = new_bn
    module._modules[trueid] = new_bn
    # param = {}
    # param["weight"] = manage_bn_module_weight[list(prun_list)].cpu().data
    # param["bias"] = manage_bn_module_bias[list(prun_list)].cpu().data
    # ti = target_id.replace(".", "-")
    # np.savez("{}/channel_bn_{}.npz".format(path,ti),**param)
    
#  剪枝全连接层
def prunLinear(model = None, target_id = None, prun_list = None, conv_kernel = None):
    
    if target_id == "None":
        return
    id_ = target_id.split(".")
    module = model
    for id in id_[:-1]:
        module = module._modules[id]
        
    preserve = set(range(conv_kernel)) - set(prun_list)
    tackle_module = module._modules[id_[-1]]
    in_features = tackle_module.in_features
    map_size = int(in_features / conv_kernel)
    preserve_linear = []
    for i in preserve:
        preserve_linear = preserve_linear + [x for x in range(i*map_size, (i+1)*map_size)]
    
    manage_linear_module_weight = tackle_module.weight
    # manage_linear_module_weight
    newLinear = torch.nn.Linear(in_features = len(preserve_linear),
                                out_features=tackle_module.out_features,
                                bias=True if tackle_module.bias != None else False)
    
    newLinear.weight = Parameter(manage_linear_module_weight[:,list(preserve_linear)].clone())
    if tackle_module.bias != None:
        newLinear.bias = Parameter(tackle_module.bias)
    module._modules[id_[-1]] = newLinear

#  剪枝结尾卷积层
def prunConv2(model = None, target_id = None, prun_list = None,path="."):
    if target_id == "None":
        return
    id_ = target_id.split(SEPARATOR)
    module = model
    trueid = ""
    for id in id_[1:-1]:
        trueid = trueid+SEPARATOR+id
        module = module._modules[trueid]
    
    # 更换删除卷积核
    # tackle_module = module._modules[id_[-1]]
    trueid = trueid+SEPARATOR+id_[-1]
    # tackle_module = module._modules[id_[-1]]
    tackle_module = module._modules[trueid]
    
    
    manage_conv_module_weight = tackle_module.weight
    preserve = set(range(manage_conv_module_weight.shape[1])) - set(prun_list)
    new_conv = None
    # ti = target_id.replace(".", "-")
    
    
    if isinstance(tackle_module, torch.nn.Conv2d):
        # param = {}
        # param["weight"] = manage_conv_module_weight[:,list(prun_list),:,:].cpu().data
        # param["bias"] = None
        # np.savez("{}/channel_conv2_{}.npz".format(path,ti),**param)
        new_conv = torch.nn.Conv2d(in_channels=len(preserve), 
                    out_channels=tackle_module.out_channels,
                    kernel_size=tackle_module.kernel_size,
                    stride=tackle_module.stride,
                    padding=tackle_module.padding,
                    bias=True if tackle_module.bias != None else False)
        new_conv.weight = Parameter(manage_conv_module_weight[:,list(preserve),:,:].clone())
        
        if tackle_module.bias != None:
            new_conv.bias = Parameter(tackle_module.bias)
        new_conv.uid = trueid
        # module._modules[id_[-1]] = new_conv
        module._modules[trueid] = new_conv
    elif isinstance(tackle_module, torch.nn.Conv1d):
        # param = {}
        # param["weight"] = manage_conv_module_weight[:,list(prun_list),:].cpu().data
        # param["bias"] = None
        # np.savez("{}/channel_conv2_{}.npz".format(path,ti),**param)
        new_conv = torch.nn.Conv1d(in_channels=len(preserve), 
                    out_channels=tackle_module.out_channels,
                    kernel_size=tackle_module.kernel_size,
                    stride=tackle_module.stride,
                    padding=tackle_module.padding,
                    bias=True if tackle_module.bias != None else False)
        new_conv.weight = Parameter(manage_conv_module_weight[:,list(preserve),:].clone())
        if tackle_module.bias != None:
            new_conv.bias = Parameter(tackle_module.bias)
        new_conv.uid = trueid
        # module._modules[id_[-1]] = new_conv
        module._modules[trueid] = new_conv
    
# 删层，用Sequetial替代原层
def remove_layer(model = None, target_id = None):
    id_ = target_id.split(".")
    module = model
    for id in id_[:-1]:
        module = module._modules[id]
    module._modules[id_[-1]] = torch.nn.Sequential()

# 修饰器，用于修饰钩子函数，方便传入节点名
def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw,name = text)
        return wrapper
    return decorator

def addConv1(model = None, target_id = None, data = None):
    id_ = target_id.split(".")
    module = model
    for id in id_[:-1]:
        module = module._modules[id]
    # 更换删除卷积核
    
    manage_module = module._modules[id_[-1]]
    kernel_total = manage_module.weight.shape[0]
    
    
    weight = manage_module.weight.clone()
    bias = manage_module.bias.clone()
    new_conv = None
    
    append = data["weight"].shape[0]
    if isinstance(manage_module,torch.nn.Conv2d):
        new_conv = torch.nn.Conv2d(in_channels=manage_module.in_channels, 
                        out_channels=kernel_total + append,
                        kernel_size=manage_module.kernel_size,
                        stride=manage_module.stride,
                        padding=manage_module.padding,
                        bias=True if manage_module.bias != None else False)
    elif isinstance(manage_module,torch.nn.Conv1d):
        new_conv = torch.nn.Conv1d(in_channels=manage_module.in_channels, 
                        out_channels=kernel_total + append,
                        kernel_size=manage_module.kernel_size,
                        stride=manage_module.stride,
                        padding=manage_module.padding,
                        bias=True if manage_module.bias != None else False)
    weight = weight.cpu().detach().numpy()
    newWeight = np.append(weight,data["weight"],0)
    new_conv.weight = Parameter(torch.from_numpy(newWeight).cuda())
    if manage_module.bias != None:
        bias = bias.cpu().detach().numpy()
        newBias = np.append(bias,data["bias"],0)
        new_conv.bias = Parameter(torch.from_numpy(newBias).cuda())
    new_conv.uid = target_id
    module._modules[id_[-1]] = new_conv

def addBn(model = None, target_id = None, data=None):
    id_ = target_id.split(".")
    module = model
    for id in id_[:-1]:
        module = module._modules[id]
    tackle_module = module._modules[id_[-1]]
    kernel_total = tackle_module.weight.shape[0]
    new_bn = None
    append = data["weight"].shape[0]
    if isinstance(tackle_module, torch.nn.BatchNorm2d):
        new_bn = torch.nn.BatchNorm2d(num_features=kernel_total + append)
    elif isinstance(tackle_module, torch.nn.BatchNorm1d):
        new_bn = torch.nn.BatchNorm1d(num_features=kernel_total + append)
    
    manage_bn_module_weight = tackle_module.weight.clone()
    manage_bn_module_bias = tackle_module.bias.clone()
    
    weight = manage_bn_module_weight.cpu().detach().numpy()
    newWeight = np.append(weight,data["weight"],0)
    new_bn.weight = Parameter(torch.from_numpy(newWeight).cuda())
    bias = manage_bn_module_bias.cpu().detach().numpy()
    newBias = np.append(bias,data["bias"],0)
    new_bn.bias = Parameter(torch.from_numpy(newBias).cuda())
    new_bn.running_mean = new_bn.running_mean.cuda()
    new_bn.running_var = new_bn.running_var.cuda()
    new_bn.uid = target_id
    module._modules[id_[-1]] = new_bn

def addConv2(model = None, target_id = None, data=None):
    id_ = target_id.split(".")
    module = model
    for id in id_[:-1]:
        module = module._modules[id]
    
    # 更换删除卷积核
    tackle_module = module._modules[id_[-1]]
    pre = [i for i in range(tackle_module.in_channels)]
    manage_conv_module_weight = tackle_module.weight
    append = data["weight"].shape[1]
    new_conv = None
    if isinstance(tackle_module, torch.nn.Conv2d):
        new_conv = torch.nn.Conv2d(in_channels=tackle_module.in_channels + append, 
                    out_channels=tackle_module.out_channels,
                    kernel_size=tackle_module.kernel_size,
                    stride=tackle_module.stride,
                    padding=tackle_module.padding,
                    bias=True if tackle_module.bias != None else False)
        weight = manage_conv_module_weight.cpu().detach().numpy()
        newWeight = np.append(weight,data["weight"],1)
        
        new_conv.weight =  Parameter(torch.from_numpy(newWeight).cuda())
        new_conv.bias = Parameter(tackle_module.bias)
        new_conv.uid = target_id
        module._modules[id_[-1]] = new_conv
    elif isinstance(tackle_module, torch.nn.Conv1d):
        new_conv = torch.nn.Conv1d(in_channels=tackle_module.in_channels + append, 
                    out_channels=tackle_module.out_channels,
                    kernel_size=tackle_module.kernel_size,
                    stride=tackle_module.stride,
                    padding=tackle_module.padding,
                    bias=True if tackle_module.bias != None else False)
        # new_conv.weight[:,list(pre),:] = manage_conv_module_weight[:,:,:].clone()
        
        weight = manage_conv_module_weight[:,:,:].clone().numpy()
        newWeight = np.append(weight,data["weight"],1)
        new_conv.weight =  Parameter(torch.from_numpy(newWeight))
        new_conv.bias = Parameter(tackle_module.bias)
        new_conv.uid = target_id
        module._modules[id_[-1]] = new_conv
# 设置dropout
def setDropout(model = None, target_id = None, pro=0):
    id_ = target_id.split(".")
    module = model
    for id in id_[:-1]:
        module = module._modules[id]
    
    manage_module = module._modules[id_[-1]]
    manage_module.p = pro

def setBatch(dataSet,batchSize):
    data_loader = torch.utils.data.DataLoader(dataset=dataSet, batch_size=batchSize, shuffle=True)
    return data_loader



# 对模型再度包装
'''
model:模型
optimizer:优化器
path:输出文件路径
modeltype:rnn?cnn?...
ct、ht:rnn隐含状态文件名
ct_shape、ht_shape(x,y,z):隐含状态大小，x->层数，y->batch,z->隐藏单元数
'''
class Pack():
    def __init__(self, model, dataSet, batchSize,trainCycle,optimizer, modeltype, path = ".", ct = None, ht = None, ct_shape = None, ht_shape = None):
        self.grad = {}  #  保存梯度
        self.handle = list()  # 保存钩子函数句柄，用于注销钩子函数
        self.features = {}  #  保存层输出
        self.model = model
        self.optimizer = optimizer
        self.rep = 0   # step计数器
        self.cycle = 20    #  一个周期内迭代步数
        self.mainPath = path
        self.structPath = path + '/model_0/model_1'
        self.path = path + '/__cache__'
        self.dataPath = self.structPath + '/0'
        self.controlpath = path + '/control.txt'   #  控制文件路径
        self.modeltype = modeltype
        self.protoOptim = {}    #  优化器参数
        self.logList = self.path + '/logList.txt'   #  记录当前保存了哪几个step的数据
        self.logScalar = self.path + '/myscalar'    #  scalar保存路径
        self.imgType = "GSI"    #  训练用图片类型
        self.cPath = self.path + "/outarray_"   #   隐状态保存路径
        self.confusion = None
        self.accmulate = 1
        self.dataSet = dataSet
        self.batchSize = batchSize
        self.trainCycle = trainCycle
        self.nodeDataPath = self.path + "/nodeLog"
        self.mutationOp = mutationOp()
        
        self.image_reconstruction = None
        self.activation_maps = []
        #  初始化隐状态保存文件
        atom = tables.Float64Atom()
        if ct:
            for j in range(ct_shape[1]):
                f = tables.open_file(self.cPath + str(j) + ct + ".h5", mode='w')
                for i in range(ct_shape[0]):
                    f.create_earray(f.root, ct + "_" + str(i), atom, (0, ct_shape[2]))
                f.close()
        if ht:
            for j in range(ht_shape[1]):
                f = tables.open_file(self.cPath + str(j) + ht + ".h5", mode='w')
                for i in range(ht_shape[0]):
                    f.create_earray(f.root, ht + "_" + str(i), atom, (0, ht_shape[2]))
                f.close()
        #  文件路径创建
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if not os.path.exists(self.logScalar):
            os.makedirs(self.logScalar)
        if not os.path.exists(self.dataPath):
            os.makedirs(self.dataPath)
        if not os.path.exists(self.nodeDataPath):
            os.makedirs(self.nodeDataPath)
        if not os.path.exists(self.mainPath+"/model_0/nodeLog"):
            os.makedirs(self.mainPath+"/model_0/nodeLog")
            
        if not os.path.exists(self.mainPath+"/graph"):
            os.makedirs(self.mainPath+"/graph")
        with open(self.logList,'w') as f:
            pass
        #  保存优化器参数
        for name in optimizer:
            output = {}
            optim = optimizer[name]
            
            allattrs = []
            for index in range(len(optim.param_groups)):
                attrs = {}
                param = optim.param_groups[index]
                for attr in param.keys():
                    if attr != 'params':
                        attrs[attr] = param[attr]
                allattrs.append(attrs)
            output['attrs'] = allattrs
            output['type'] = type(optim).__name__
            self.protoOptim[name] = output
        torch.save(self.model,path + "/model_0/model_0.pt")
        # shutil.copyfile(path+"/../model.json",path+"/model_0/model.json")
        with open(path + "/model_0/loss.txt","w") as f:
            pass
        with open(path + "/model_0/accuracy.txt","w") as f:
            pass
        with open(path + "/model_0/logList.txt","w") as f:
            pass
        #  初始化控制文件， 读取控制(n/r)@模型类型@模型训练运行控制(s/p)@周期@优化器参数@节点名称@监听节点@相关节点@剪枝通道@保存/读取标志(1/2/default:0)@当前模型路径@当前数据路径@dropout层@batchsize@迭代次数
        with open(self.controlpath,'w') as f:
            f.write("n@"+modeltype+"@p@" + str(self.cycle) + "@" + json.dumps(self.protoOptim) + '@@[]@[]@[]@0@' + self.structPath + "@" + self.dataPath + "@@" + str(self.batchSize) + '@' + str(self.trainCycle))
        with open(path + "/model_0/control.txt","w") as f:
            f.write("n@"+modeltype+"@p@" + str(self.cycle) + "@" + json.dumps(self.protoOptim) + '@@[]@[]@[]@0@' + self.structPath + "@" + self.dataPath + "@@" + str(self.batchSize) + '@' + str(self.trainCycle))
        
    # 全局注册钩子函数
    def regist_handle_global(self):
        grad = self.grad
        features = self.features
        # 钩子函数
        def get_features_hook(self,input,output,name):
            name = self.uid if hasattr(self,'uid') else name
            if name in features.keys():
                features[name].append(output)
            else:
                features[name] = []
                features[name].append(output)
            # features[name] = output
        def get_grad_hook(self,input,output,name):
            name = self.uid if hasattr(self,'uid') else name
            name_ = name + "_back"
            if name_ in grad.keys():
                
                grad[name_].append(output[0])
            else:
                grad[name_] = []
                grad[name_].append(output[0])
            # grad[name + "_back"] = output[0]
        def get_model_hook(self,input,output):# self 代表类模块本身
            features["modelOutput"] = [output]
            features["modelInput"] = [input[0]]
            
        h = self.model.register_forward_hook(get_model_hook)
        self.handle.append(h)
        # 遍历模块注册钩子函数，注：function无法监听
        def reveal(module,name):
            
            for i in module._modules.keys():
                tmpName = ''
                if name == ' ':
                    tmpName = i
                else:
                    tmpName = name + '.' + i
                tmpModule = module._modules[i]
                Get_feature_hook = log(tmpName)(get_features_hook)
                h = tmpModule.register_forward_hook(Get_feature_hook)
                Get_grad_hook = log(tmpName)(get_grad_hook)
                h1 = tmpModule.register_backward_hook(Get_grad_hook)
                self.handle.append(h)
                self.handle.append(h1)
                reveal(tmpModule, tmpName)
        reveal(self.model, ' ')
    
    # 释放钩子函数
    def remove_handle(self):
        for i in self.handle:
            i.remove()
        self.handle = []
            
    # 保存权重，偏置，梯度，特征
    def save_data(self,scalarParam,keep):
        # 一个周期结束，保存参数
        self.rep += 1
        if (self.rep % self.cycle) == 0 and (self.rep != 0) and keep != "2":
            dic = {}
            for param in self.model.named_parameters():
                name = param[0]
                name_ = name.split('.')
                name = '.'.join(name_[:-1])
                
                if name in self.monitorList:
                    dic[param[0]] = param[1].cpu().data
                    dic[param[0]+'_grad'] = param[1].grad.cpu().data

            for param in self.features.keys():
                if param in self.monitorList:
                    r = re.search("(\(\d+\))",param)
                    if r == None:
                        dic[param] = self.features[param][0].cpu().data
                    else:
                        index = int(r.groups()[0][1:-1])
                        param_ = param.split("(")[0]
                        dic[param] = self.features[param][index].cpu().data
                    
            dic["step"] = self.rep

            np.savez(self.dataPath + '/result_' + str(self.rep) +'.npz', **dic)
            
            with open(self.logList,'a') as f:
                f.write('result_' + str(self.rep) +'.npz' + '\n')

            # 保存标量
            if scalarParam:
                for i in scalarParam.keys():
                        path = self.logScalar + '/' + i +'.txt'
                        digit = scalarParam[i]
                        if isinstance(scalarParam[i],torch.Tensor):
                            digit = digit.cpu().detach().numpy()
                        par = str(digit) + ',' + str(self.rep) + '\n'
                        with open(path,'a') as f:
                            f.write(par)
            for name in self.monitorList:
                with open("{}/{}.text".format(self.nodeDataPath,name),"a") as f:
                    f.write(str(self.rep) + "\n")
        
            
                        



            
    # 循环控制,保存输入标量
    def control(self,scalarParam = None,dataList=None,predict=None,groundTruth=None):
        f = open(self.controlpath,'r')
        controldata = f.readline()
        f.close()
        
        #  读取控制信息
        try:
            [readtag,modeltype,tag, cycle, paramConq,nodeId,monitorList,appendix,prunList,keep,structPath,dataPath,dropout,batchSize,trainCycle] = controldata.split('@')
            
            self.monitorList = json.loads(monitorList)
            # self.monitorList = []
            self.appendix = json.loads(appendix)
            
            self.prunList = json.loads(prunList)
            w = open(self.controlpath,'w')
            dataSetLoader = None
            trainCyclen = None
            if int(batchSize) != self.batchSize:
                self.batchSize = int(batchSize)
                dataSetLoader = setBatch(self.dataSet,self.batchSize)
            # if int(trainCycle) != self.trainCycle:
            #     self.trainCycle = int(trainCycle)
            #     trainCyclen = int(trainCycle)
            self.trainCycle = int(trainCycle)
            if dropout:
                target = dropout.split("=")[0]
                pro = float(dropout.split("=")[1])
                setDropout(self.model,target,pro)
            # '''
            prunTag = "n"
            if len(self.prunList) > 0:
                prunTarget = None
                with open(self.mainPath + "/prunTarget.json","r") as fp:
                    prunTarget = json.load(fp)
                # graph_ = self.prun(prunTarget)
                self.prun(prunTarget)
                # prunTag = "y"
                self.action("1",structPath,dataPath,"outer")
                
            else:
                self.action(keep,structPath,dataPath,"outer")
            
            self.prunList = []
            dic = {}
            
            
            #  控制信息为读取时,数据读取时使用nodeId_，存储时使用nodeId，index区分第几个数据
            if readtag == 'r':
                r = re.search("(\(\d+\))",nodeId)
                index = 0
                nodeId_ = nodeId
                
                if r != None:
                    index = int(r.groups()[0][1:-1])
                    param_ = nodeId.split("(")[0]
                    nodeId_ = param_
                    
                
                for param in self.model.named_parameters():
                    ID = param[0]
                    ID = ID.split('.')
                    ID = ID[:-1]
                    ID = '.'.join(ID)
                    if ID == nodeId_ or ID in self.appendix:
                        dic[param[0]] = param[1].cpu().data
                        dic[param[0]+'_grad'] = param[1].grad.cpu().data
                if nodeId_ in self.features:
                    dic[nodeId] = self.features[nodeId_][index].cpu().data
                if nodeId_+"_back" in self.grad:
                    dic[nodeId+"_back"] = self.grad[nodeId_+"_back"][len(self.grad[nodeId_+"_back"])-1-index].cpu().data
                
                for ID in self.appendix:
                    if ID == "None":
                        continue
                    r = re.search("(\(\d+\))",ID)
                    indexID = 0
                    ID_ = ID
                    if r != None:
                        indexID = int(r.groups()[0][1:-1])
                        param_ = ID.split("(")[0]
                        ID_ = param_
                    dic[ID] = self.features[ID_][indexID].cpu().data
                    dic[ID+"_back"] = self.grad[ID_+"_back"][len(self.grad[ID_+"_back"])-1-indexID].cpu().data
                dic["step"] = self.rep + 1
                #  储存临时信息
                np.savez(self.dataPath + '/result.npz', **dic)
                #  周期未结束时读取信息，logList写入记录
                if ((self.rep + 1) % self.cycle) != 0 and keep != "2":
                    np.savez(self.dataPath + '/result_'+ str(self.rep+1) +'.npz', **dic)
                    self.logListW = open(self.logList,'a')
                    self.logListW.write('result_' + str(self.rep+1) +'.npz' + '\n')
                    self.logListW.close()
                    for i in scalarParam.keys():
                        path = self.logScalar + '/' + i +'.txt'
                        digit = scalarParam[i]
                        if isinstance(scalarParam[i],torch.Tensor):
                            digit = digit.cpu().detach().numpy()
                        par = str(digit) + ',' + str(self.rep + 1) + '\n'
                        tmp = open(path,'a')
                        tmp.write(par)
                        tmp.close()
                    for name in self.monitorList:
                        with open("{}/{}.text".format(self.nodeDataPath,name),"a") as f:
                            f.write(str(self.rep+1) + "\n")

                tag = 's'
                
                # ! r要改成n
            self.save_data(scalarParam,keep)
            
            # self.action(keep,structPath,dataPath)
            # if len(self.prunList) > 0: 
            #     self.prun(nodeId)
            
            # w.write('n@' + modeltype + '@' + tag + '@' + cycle + '@' + paramConq + '@' + nodeId + '@' + monitorList + '@' + appendix + '@' + '[]')
            w.write("@".join(['n',modeltype,tag,cycle,paramConq,nodeId,monitorList,appendix,'[]','0',self.structPath,self.dataPath,'',str(self.batchSize),str(self.trainCycle)]))
            w.close()
            
            
            f = open(self.controlpath,'r')
            params = json.loads(paramConq)
            #  训练过程暂停
            if tag == 's':
                while True:
                    f.seek(0,0)
                    controldata = f.readline()
                    readtag,modeltype,tag, cycle, paramConq,nodeId,monitorList,appendix,prunList,keep,structPath,dataPath,dropout,batchsize,trainCycle = controldata.split('@')
                    if tag == 'p':
                        break
                    time.sleep(5)
            f.close()
            cycle = int(cycle)
            # ! 修改cycle
            if self.cycle != cycle:
                self.cycle = cycle
            #     self.rep = 0
                
            
            #  修改优化器参数
            for name in params.keys():
                optim = self.optimizer[name]
                params = params[name]['attrs']
                for optim_param_group_index in range(len(optim.param_groups)):
                    optim_param_group = optim.param_groups[optim_param_group_index]
                    params_param_group = params[optim_param_group_index]
                    for key in params_param_group:
                        optim_param_group[key] = params_param_group[key]
            
            for i in self.features.keys():
                self.features[i].clear()
            for i in self.grad.keys():
                self.grad[i].clear()
            self.remove_handle()
            self.regist_handle_global()
            torch.cuda.empty_cache()
            gc.collect()
            # print(self.grad.keys())
            return (self.trainCycle,dataSetLoader,self.model,prunTag,structPath,dataPath)
        except Exception as e:
            print(e)
            return (None,None,None,None,None,None)
    
    
    def action(self,tag,path,dataPath,user="inner",graph_=None):
        # 保存训练节点: ../model_6 -> ../model_6/model_7, ../model_6/5 _> ../model_6/model_7/0
        if tag == '1':
            self.accmulate += 1
            
            tmpPath = self.structPath
            self.structPath = self.structPath + "/model_{}".format(self.accmulate)
            # 保存步数
            with open(self.dataPath + "/re.text",'w') as f:
                f.write(str(self.rep))
            self.dataPath = self.structPath + "/0"
            os.makedirs(self.structPath)
            os.makedirs(self.dataPath)
            self.remove_handle()
            modelPath = "{}/model_{}.pt".format(tmpPath,self.accmulate-1)
            torch.save(self.model,modelPath)
            # !
            # self.model = torch.load(modelPath,map_location='cuda:0')
            # ！
            print('save',modelPath)
            # graph(self.model,self.features["modelInput"][0],tmpPath,self.accmulate,tag=False)
            # torch.save(self.model,"{}/model_{}.pt".format(tmpPath,self.accmulate-1))
            
            shutil.copyfile(self.logScalar + "/accuracy.txt",tmpPath + "/accuracy.txt")
            shutil.copyfile(self.logScalar + "/loss.txt",tmpPath + "/loss.txt")
            shutil.copyfile(self.logList,tmpPath + "/logList.txt")
            shutil.copyfile(self.controlpath,tmpPath + "/control.txt")
            # if graph_:
            #     with open(tmpPath + "/model.json","w") as f:
            #         f.write(json.dumps(graph_))
            #     with open(self.mainPath + "/../model.json", "w") as f:
            #         f.write(json.dumps(graph_))
            # else:
            #     shutil.copyfile(self.mainPath + "/../model.json",tmpPath + "/model.json")
            
            shutil.copytree(self.nodeDataPath,tmpPath + "/nodeLog")
            # self.model = None
            # self.model = torch.load(modelPath,map_location='cuda:0')
            # self.optimizer["vgg16"].param_groups[0]["params"] = list(self.model.parameters())
            self.regist_handle_global()
        # 重新载入训练节点: ../model_6 -> ../model_1/model_7, ../model_6/5 -> ../model_1/model_7/0
        elif tag == "2":
            if user == "outer":
                self.accmulate += 1
                self.structPath = path + "/model_" + str(self.accmulate)
                # 步数重置
                file_list = os.listdir(path)
                def detect(name):
                    return not("model_" in name or ".pt" in name or ".json" in name or ".txt" in name or "Log" in name)
                files = list(filter(detect,file_list))
                try:
                    with open(path + "/" + str(len(files)-1) + "/re.text") as f:
                        self.rep = int(f.readline().strip())
                        print(path + "/" + str(len(files)-1) + "/re.text","rep",self.rep)
                except Exception:
                    print(path + "/" + str(len(files)-1) + "/re.text")
                    self.rep = 0
                print("rep",self.rep)
                # print(files)
                self.dataPath = self.structPath + "/0"
                pathSeg = path.split("/")
                modelPath = path + "/" + pathSeg[-1] + '.pt'
                
                os.makedirs(self.structPath)
                os.makedirs(self.dataPath)
                self.remove_handle()
                self.model = torch.load(modelPath,map_location='cuda:0')
                print('load',modelPath)
                self.optimizer[self.modeltype].param_groups[0]["params"] = list(self.model.parameters())
                shutil.copyfile(path + "/accuracy.txt",self.logScalar + "/accuracy.txt")
                shutil.copyfile(path + "/loss.txt",self.logScalar + "/loss.txt")
                shutil.copyfile(path + "/logList.txt",self.logList)
                shutil.copyfile(path + "/control.txt",self.controlpath)
                # shutil.copyfile(path + "/model.json",self.mainPath + "/../model.json")
                self.regist_handle_global()
                
                print("重载成功")
                shutil.rmtree(self.nodeDataPath)
                shutil.copytree(path + "/nodeLog",self.path + "/nodeLog")
            else:
                self.remove_handle()
                pathSeg = path.split("/")
                modelPath = path + "/" + pathSeg[-1] + '.pt'
                self.model = torch.load(modelPath,map_location='cuda:0')
                self.optimizer[self.modeltype].param_groups[0]["params"] = list(self.model.parameters())
                self.regist_handle_global()
        # 剪枝复原
        elif tag == "3":
            self.dataPath = dataPath
            self.restore(dataPath)
            
    # 剪枝: ../5 -> ../6
    def prun(self,nodeId):
        self.remove_handle()
        # shape = self.features["modelInput"][0].shape
        # graph(self.model,torch.randn([1,shape[1],shape[2],shape[3]]).cuda(),self.dataPath,tag=False)
        shutil.copytree(self.nodeDataPath,self.dataPath+"/nodeLog")
        with open(self.dataPath + "/re.text",'w') as f:
            f.write(str(self.rep))
        
        # channels = prunConv1(self.model,nodeId,self.prunList,self.dataPath)
        # graph_m = None
        # graph_o = None
        # kernel_ = 
        # with open(self.structPath + "/../model.json", "r") as f:
        #     graph_m = json.load(f)
        # with open(self.structPath + "/../model.json", "r") as f:
        #     graph_o = json.load(f)
            # graph_o = json.load(f)
        # channel = int(graph_o[nodeId]["attr"]["out_channels"]) - len(self.prunList)
        # self.mutationOp.modify_channel(graph_m,nodeId,channel)
        
        
        
        # print(graph_m)
        
        # TODO
        # if self.appendix[0] != "None":
        #     prunBn(self.model,self.appendix[0],self.prunList,self.dataPath)
        # if self.appendix[2] != "None":
        #     prunConv2(self.model,self.appendix[2],self.prunList,self.dataPath)
        # if self.appendix[3] != "None":
        #     prunLinear(self.model,self.appendix[3],self.prunList,channels)
        # try:
        #     for key in graph_m.keys():
        #         if graph_m[key]["type"] == "conv2d":
        #             if graph_m[key]["attr"]["in_channels"] != graph_o[key]["attr"]["in_channels"]:
        #                 prunConv2(self.model,key,self.prunList,self.dataPath)
        #             elif graph_m[key]["attr"]["out_channels"] != graph_o[key]["attr"]["out_channels"]:
        #                 prunConv1(self.model,key,self.prunList,self.dataPath)
        #         if graph_m[key]["type"] == "bn2d":
        #             if graph_m[key]["attr"]["num_features"] != graph_o[key]["attr"]["num_features"]:
        #                 prunBn(self.model,key,self.prunList,self.dataPath)
        # except Exception as e:
        #     print(e)
        
        conv1 = nodeId["conv1"]
        bn2d = nodeId["bn2d"]
        conv2 = nodeId["conv2"]
        prunConv1(self.model,conv1,self.prunList,self.dataPath)
        prunBn(self.model,bn2d,self.prunList,self.dataPath)
        prunConv2(self.model,conv2,self.prunList,self.dataPath)
        
        seg = self.dataPath.split("/")
        index = int(seg[-1]) + 1
        seg[-1] = str(index)
        self.dataPath = "/".join(seg)
        os.makedirs(self.dataPath)
        
        
        self.regist_handle_global()
        # 优化器参数重置
        self.optimizer[self.modeltype].param_groups[0]["params"] = list(self.model.parameters())
        print(self.model)
        # return graph_m
        
        
        
    # 剪枝复原: ../5 -> ../2
    # dataPath:数据储存路径
    def restore(self,dataPath):
        seg = dataPath.split("/")
        def number(name):
            return not("model_" in name or ".pt" in name or ".json" in name)
        
        v = list(filter(number,os.listdir(self.structPath)))
        index = int(seg[-1])
        for i in range(len(v)-2,index,-1):
            seg[-1] = str(i)
            path = "/".join(seg)
            self.addChannel(path)
        self.remove_handle()
        self.regist_handle_global()
        self.moveDataFiles(dataPath)
        # 重新生成路径
        seg = self.dataPath.split("/")
        index = int(seg[-1]) + 1
        seg[-1] = str(index)
        self.dataPath = "/".join(seg)
        os.makedirs(self.dataPath)
    
    def moveDataFiles(self,dataPath):
        seg = dataPath.split("/")
        file_list = os.listdir(self.structPath)
        def dataStore(name):
            return not("model" in name or ".pt" in name or ".json" in name)
        files = list(filter(dataStore,file_list))
        end = int(seg[-1])
        def dataFile(name):
            return "result_" in name
        dstPath = dataPath
        for i in range(len(files)-1,end,-1):
            dataPath = self.structPath + "/" + str(i)
            dataFileList = os.listdir(dataPath)
            dataFiles = filter(dataFile,dataFileList)
            for j in dataFiles:
                srcPath = dataPath + "/" + j
                move(srcPath,dstPath)
            shutil.rmtree(dataPath)
        shutil.rmtree(dstPath+"/nodeLog")
        shutil.copytree(self.nodeDataPath,dstPath+"/nodeLog")
    
    # 恢复通道数据
    # channleDataPath:剪枝文件夹路径
    # 通道参数文件名：channel=conv1=节点名.npz
    def addChannel(self,channleDataPath):
        # pass
        def channel(n):
            return "channel" in n
        
        v = list(filter(channel,os.listdir(channleDataPath)))
        
        for i in v:
            seg = i.split("_")
            nodeId = seg[-1].replace("-", ".")[:-4]
            dataPath = channleDataPath + "/" + i
            data = np.load(dataPath)
            channelData = data
            # print(channelData)
            if "conv1" in i:
                addConv1(self.model,nodeId,channelData)
            if "bn" in i:
                addBn(self.model,nodeId,channelData)
            if "conv2" in i:
                addConv2(self.model,nodeId,channelData)
                
        
        