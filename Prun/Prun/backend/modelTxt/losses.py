
# 损失函数获取

import torch.nn as nn

class LossGetter():
    @staticmethod
    def L1Loss():
        return nn.L1Loss()
    @staticmethod
    def CrossEntropyLoss():
        return nn.CrossEntropyLoss()

    @staticmethod
    def SmoothL1Loss():
        return nn.SmoothL1Loss()

    @staticmethod
    def MSELoss():
        return nn.MSELoss()
    
    @staticmethod
    def BCELoss():
        return nn.BCELoss()
    
    @staticmethod
    def BCEWithLogitsLoss():
        return nn.BCEWithLogitsLoss()
    @staticmethod
    def NLLLoss():
        return nn.NLLLoss()
    
    @staticmethod
    def NLLLoss2d():
        return nn.NLLLoss2d()
    
    @staticmethod
    def KLDivLoss():
        return nn.KLDivLoss()
    
    @staticmethod
    def MarginRankingLoss():
        return nn.MarginRankingLoss()
    
    @staticmethod
    def MultiMarginLoss():
        return nn.MultiMarginLoss()
    
    @staticmethod
    def MultiLabelMarginLoss():
        return nn.MultiLabelMarginLoss()
    
    @staticmethod
    def SoftMarginLoss():
        return nn.SoftMarginLoss()
    
    @staticmethod
    def MultiLabelSoftMarginLoss():
        return nn.MultiLabelSoftMarginLoss()
    
    @staticmethod
    def CosineEmbeddingLoss():
        return nn.CosineEmbeddingLoss()
    
    
    
    '''统一管理'''
    @staticmethod
    def getLoss(type):
        loss = LossGetter().__getattribute__(type)()
        return loss