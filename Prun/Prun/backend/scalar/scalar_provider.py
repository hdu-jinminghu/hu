'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-11-22 15:39:41
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
from .scalar_reader import *
def get_scalar_data(request):
    job = request.GET.get("job")
    data = None
    try:
        data = scalar_read(job)
    except FileNotFoundError as e:
        return {"tol":[[]],"breakpoints":[]}
    return data