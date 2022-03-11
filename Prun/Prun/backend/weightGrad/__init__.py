'''
Author: your name
Date: 2021-03-29 09:36:25
LastEditTime: 2021-04-08 10:32:45
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\__intit__.py
'''
__all__ = [
    "weightGrad_read","get_weightGrad_data"]

from .weightGrad_reader import weightGrad_read
from .weightGrad_provider import get_weightGrad_data