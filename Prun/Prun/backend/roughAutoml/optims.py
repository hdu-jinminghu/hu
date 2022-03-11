# 优化器获取

import torch.optim as optim

class OptimGetter():
    @staticmethod
    def adam():
        return optim.Adam
    @staticmethod
    def adadelta():
        return optim.Adadelta

    @staticmethod
    def adagrad():
        return optim.Adagrad

    @staticmethod
    def adamax():
        return optim.Adamax
    
    @staticmethod
    def rmsprop():
        return optim.RMSprop
    
    @staticmethod
    def rprop():
        return optim.Rprop
    @staticmethod
    def sgd():
        return optim.SGD
    
    '''统一管理'''
    @staticmethod
    def getOptim(type):
        optim = OptimGetter().__getattribute__(type)()
        return optim