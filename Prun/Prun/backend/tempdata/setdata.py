'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-04-21 15:52:26
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
from .set_data import *
def set_node_data(request):
    job = request.GET.get('job')
    id = request.GET.get('Id')
    appendix = request.GET.get('appendix')
    data = set_node(job ,id,appendix)
    return data
