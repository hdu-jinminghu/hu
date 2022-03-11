'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-04-21 14:29:48
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
from .sensitivity_reader import sensitivity_read
def get_sensitivity_data(request):
    job = request.GET.get('job')
    id = request.GET.get('Id')
    step = request.GET.get('step')
    data = sensitivity_read(job, id, step)
    return data
