
import torch.optim as optim
import torch.utils.data
import torch.backends.cudnn as cudnn
import torchvision
from torchvision import transforms as transforms
import numpy as np
import torch
import torch.nn as nn
import os
import time
import torch.nn.functional as F
import json

from .misc import progress_bar
from .compile import createModel
from Prun.backend.utils import getPath
from .optims import OptimGetter
from .losses import LossGetter
from .utils.utils import graph,Pack
from .datasets import DatasetGetter

class Solver(object):
    def __init__(self):
        self.model = None
        self.device = None
        self.epoch = 0
        self.trainEpoches = 1000000
        self.lr = 0.01
        self.train_batch_size = 50
    def store_image(self, path, data):
        for i in range(data.shape[0]):
            img1 = transforms.ToPILImage()(data[i,:,:,:])
            img1.save("{}/{}.jpg".format(path, i))
    # 加载数据集  
    def load_data(self,dataset):
        self.train_set = DatasetGetter.getDataset(dataset)
        self.train_loader = torch.utils.data.DataLoader(dataset=self.train_set, batch_size=self.train_batch_size, shuffle=True)
        self.test_data_path = getPath('./data/{}/image'.format(dataset))
        if not os.path.exists(self.test_data_path):
            os.makedirs(self.test_data_path)
        for batch_num, (data, target) in enumerate(self.train_loader):
            self.store_image(self.test_data_path, data)
            break
        
    def load_config(self,lossFc):
        optimizer = OptimGetter.getOptim("SGD")
        self.optimizer = optimizer(self.model.parameters(), lr=self.lr)
        self.criterion = LossGetter.getLoss(lossFc).to(self.device)
        
    # 加载模型
    def load_model(self,model):
        cudnn.benchmark = True
        self.device = torch.device('cuda')
        self.model = model
        self.model.to(self.device)
    
    def wrap_model(self,dPath,job):
        
        for batch_num, (data, target) in enumerate(self.train_loader):
            graph(self.model,data.to(self.device),path=dPath)
            break
            
        self.model_ = Pack(self.model,self.train_set,self.train_batch_size,5000,{job:self.optimizer},job,path=dPath)
    # 模型训练
    def train(self):
        self.model.train()
        train_loss = 0
        train_correct = 0
        total = 0
        for batch_num, (data, target) in enumerate(self.train_loader):
            self.epoch += 1
            data, target = data.to(self.device), target.to(self.device)
            self.optimizer.zero_grad()
            self.model.zero_grad()
            output = self.model(data)

            prediction = torch.max(output, 1)  
            total_ = target.size(0)
            total += target.size(0)

            loss = self.criterion(output, target)
            loss.backward()
            
            self.optimizer.step()
            train_loss_ = loss.item()
            train_loss += train_loss_

            train_correct_ = np.sum(prediction[1].cpu().numpy() == target.cpu().numpy())
            train_correct += train_correct_
            if batch_num == 0:
                with open("{}/{}".format(self.test_data_path,"res.txt"),"w") as f:
                    res = []
                    for (i,j) in zip(prediction[1].cpu().numpy(), target.cpu().numpy()):
                        res.append([int(i),int(j)])
                    f.write(json.dumps(res))
                    
                
            self.optimizer.zero_grad()
            self.model.zero_grad()          
            # (trainCycle,dataSetLoader,model,prunTag,structPath,dataPath) = self.model_.control({"accuracy":100. * train_correct / total,"loss":(train_loss / (batch_num + 1))})
            (trainCycle,dataSetLoader,model,prunTag,structPath,dataPath) = self.model_.control({"accuracy":100. * train_correct_/total_,"loss":(train_loss_)})
            progress_bar(batch_num, len(self.train_loader), 'Loss: %.4f | Acc: %.3f%% (%d/%d)'
                         % (train_loss / (batch_num + 1), 100. * train_correct / total, train_correct, total))
            # self.trainEpoches = trainCycle
            # if trainCycle == None:
            #     continue
            if dataSetLoader:
                self.train_loader = dataSetLoader
                break
            if self.model != model:
                if model:
                    self.model = model
                break
            # if prunTag == "y":
            #     self.model_.action("2",structPath,dataPath)
            #     self.model = self.model_.model
            #     break
        

def start(model,dPath,lossFc,dataset,job):
    solver = Solver()
    solver.load_data(dataset)
    solver.load_model(model)
    solver.load_config(lossFc)
    solver.wrap_model(dPath,job)
    
    while solver.epoch < solver.trainEpoches:
        solver.train()

def buildModel(lossFc,dataset,job,g):
    model = None
    if g=='generator':
        time.sleep(1)
        path = getPath("./Prun/data/model.json")
        model = createModel(path)
    elif g=='reload':
        path = getPath('./Prun/data/{}/model_0/model_0.pt'.format(job))
        model = torch.load(path,map_location='cuda:0')
        scalarPath = getPath('./Prun/data/{}/__cache__/myscalar'.format(job))
        with open('{}/accuracy.txt'.format(scalarPath),"w") as f:
            # f.write('')
            pass
        with open('{}/loss.txt'.format(scalarPath),"w") as f:
            # f.write('')
            pass
        
    # path = getPath("./Prun/data/model.json")
    # model = createModel(path)
    # model = Net()
    print(model)
    dPath = getPath("./Prun/data/{}".format(job))
    start(model,dPath,lossFc,dataset,job)

    