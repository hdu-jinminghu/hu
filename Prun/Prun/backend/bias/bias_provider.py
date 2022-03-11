'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-09-14 20:56:05
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''

from .bias_reader import *
def get_bias_data(request):
    job = request.GET.get("job")
    id = request.GET.get("Id")
    tag = request.GET.get("tag")
    index = request.GET.get("index")
    npzPath = request.GET.get("npzPath")
    data = bias_read(job, id, tag, index,npzPath)
    return data
