'''
Author: your name
Date: 2021-03-29 09:36:25
LastEditTime: 2021-04-08 15:32:30
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\__intit__.py
'''
__all__ = [
    "get_contorl_data","data_read","change_control"]

from .control_provider import get_contorl_data
from .control_reader import data_read
from .change_control_data import change_control