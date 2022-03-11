'''
Author: your name
Date: 2021-03-29 09:36:25
LastEditTime: 2021-04-07 10:12:49
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\__intit__.py
'''
__all__ = [
    "get_rank_data","get_data","rank","rank_read"]

from .rank_reader import get_data,rank,rank_read
from .rank_provider import get_rank_data