
import torchvision
from torchvision import transforms as transforms


class DatasetGetter():
    @staticmethod
    def MNIST():
        torchvision.datasets.MNIST(root='./data', train=False,download=True, transform = transforms.ToTensor())
        return torchvision.datasets.MNIST(root='./data', train=True, download=True,transform = transforms.ToTensor())
    @staticmethod
    def CIFAR10():
        torchvision.datasets.CIFAR10(root='./data', train=False,download=True, transform = transforms.ToTensor())
        return torchvision.datasets.CIFAR10(root='./data', train=True, download=True,transform = transforms.ToTensor())
    
    '''统一管理'''
    @staticmethod
    def getDataset(type):
        dataset = DatasetGetter().__getattribute__(type)()
        return dataset