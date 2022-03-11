'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2021-04-07 16:03:55
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
from .parameters_reader import parameters_read
def get_parameters_data(request):
    job = request.GET.get('job')
    data = parameters_read(job)
    return data
    