'''
Author: your name
Date: 2021-03-29 09:36:25
LastEditTime: 2021-04-08 10:46:25
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\__intit__.py
'''
__all__ = [
    "bias_read","get_bias_data"]

from .bias_reader import bias_read
from .bias_provider import get_bias_data