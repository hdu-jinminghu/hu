'''
Author: your name
Date: 2021-03-24 09:47:39
LastEditTime: 2021-03-24 14:53:56
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\data_provider\searcher.py
'''
import os
def file_searcher(request):
    file_list = os.listdir("./Prun/data")
    return file_list
    