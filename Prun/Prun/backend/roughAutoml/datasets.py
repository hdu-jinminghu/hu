
import torchvision
from torchvision import transforms as transforms


class DatasetGetter():
    @staticmethod
    def MNIST():
        testSet = torchvision.datasets.MNIST(root='./data', train=False,download=True, transform = transforms.ToTensor())
        trainSet = torchvision.datasets.MNIST(root='./data', train=True, download=True,transform = transforms.ToTensor())
        return (trainSet,testSet)
    @staticmethod
    def CIFAR10():
        testSet = torchvision.datasets.CIFAR10(root='./data', train=False,download=True, transform = transforms.ToTensor())
        trainSet = torchvision.datasets.CIFAR10(root='./data', train=True, download=True,transform = transforms.ToTensor())
        return (trainSet,testSet)
    
    '''统一管理'''
    @staticmethod
    def getDataset(type):
        dataset = DatasetGetter().__getattribute__(type)()
        return dataset