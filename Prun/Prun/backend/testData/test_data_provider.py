'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-11-19 11:16:42
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
from .test_data_reader import data_reader
def get_test_data(request):
    job = request.GET.get("job")
    dataset = request.GET.get("dataset")
    data = data_reader(job, dataset)
    return data