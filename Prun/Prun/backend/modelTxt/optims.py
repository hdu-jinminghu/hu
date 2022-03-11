# 优化器获取

import torch.optim as optim

class OptimGetter():
    @staticmethod
    def Adam():
        return optim.Adam
    @staticmethod
    def Adadelta():
        return optim.Adadelta

    @staticmethod
    def Adagrad():
        return optim.Adagrad

    @staticmethod
    def Adamax():
        return optim.Adamax
    
    @staticmethod
    def RMSprop():
        return optim.RMSprop
    
    @staticmethod
    def Rprop():
        return optim.Rprop
    @staticmethod
    def SGD():
        return optim.SGD
    
    '''统一管理'''
    @staticmethod
    def getOptim(type):
        optim = OptimGetter().__getattribute__(type)()
        return optim