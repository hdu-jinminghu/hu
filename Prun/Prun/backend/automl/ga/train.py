'''
Author: your name
Date: 2021-12-13 09:57:10
LastEditTime: 2021-12-13 14:56:12
LastEditors: your name
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \Prun\Prun\backend\automl\ga\train.py
'''
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

from .optims import OptimGetter
from .losses import LossGetter
from .datasets import DatasetGetter
from .misc import progress_bar


class Trainer():
    def __init__(self,model,epoch=10,batch_size=200,optim="sgd",lossFc="CrossEntropyLoss",dataset="CIFAR10"):
        self.device = "cuda"
        self.model = model
        self.model.to(self.device)
        self.epoch = epoch
        optimizer = OptimGetter.getOptim(optim)
        self.optimizer = optimizer(self.model.parameters(), lr=0.01)
        self.criterion = LossGetter.getLoss(lossFc).to(self.device)
        self.train_batch_size = batch_size
        self.load_data(dataset)
    
    # 加载数据集  
    def load_data(self,dataset):
        self.train_set = DatasetGetter.getDataset(dataset)
        self.train_loader = torch.utils.data.DataLoader(dataset=self.train_set, batch_size=self.train_batch_size, shuffle=True)

    def train_one_epoch(self):
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
            total += target.size(0)

            loss = self.criterion(output, target)
            loss.backward()
            
            self.optimizer.step()
            train_loss += loss.item()

            train_correct += np.sum(prediction[1].cpu().numpy() == target.cpu().numpy())
                    
                
            self.optimizer.zero_grad()
            self.model.zero_grad()          

            progress_bar(batch_num, len(self.train_loader), 'Loss: %.4f | Acc: %.3f%% (%d/%d)'
                         % (train_loss / (batch_num + 1), 100. * train_correct / total, train_correct, total))
        return (100. * train_correct / total, train_loss / (batch_num + 1))
    
    def train(self):
        res = 0
        for i in range(self.epoch):
            
            res = self.train_one_epoch()
        return res
