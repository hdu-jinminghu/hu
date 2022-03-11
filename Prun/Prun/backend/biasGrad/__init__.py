'''
Author: your name
Date: 2021-03-29 09:36:25
LastEditTime: 2021-04-08 11:07:19
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\__intit__.py
'''
__all__ = [
    "biasGrad_read","get_biasGrad_data"]

from .biasGrad_reader import biasGrad_read
from .biasGrad_provider import get_biasGrad_data