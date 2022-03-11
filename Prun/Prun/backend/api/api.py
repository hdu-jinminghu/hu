'''
Author: your name
Date: 2021-03-23 19:27:37
LastEditTime: 2022-01-10 20:22:40
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\api\api.py
'''

from django.views.decorators.gzip import gzip_page
from .utils import *
from Prun.backend.data_provider import *
from Prun.backend.rank import *
from Prun.backend.parameters import *
from Prun.backend.sensitivity import *
from Prun.backend.weight import *
from Prun.backend.weightGrad import *
from Prun.backend.bias import *
from Prun.backend.biasGrad import *
from Prun.backend.scalar import *
from Prun.backend.control import *
from Prun.backend.monitor import *
from Prun.backend.cycle import *
from Prun.backend.tempdata import *
from Prun.backend.prun import *
from Prun.backend.play import *
from Prun.backend.dropout import *
from Prun.backend.batchsize import *
from Prun.backend.trainCycle import *
from Prun.backend.lr import *
from Prun.backend.keep import *
from Prun.backend.trainData import *
from Prun.backend.modelTxt import *
from Prun.backend.testData import *
from Prun.backend.automlList import *
from Prun.backend.automlGraph import *
from Prun.backend.automl import *
from Prun.backend.roughAutoml import *
from Prun.backend.graph import *


# @gzip_page
@response_wrapper
def get_graph(request):
    return validate_get_request(request, graph_reader)

@gzip_page
@response_wrapper
def get_all_file(request):
    return validate_get_request(request, file_searcher)

@gzip_page
@response_wrapper
def get_rank(request):
    return validate_get_request(request, get_rank_data)

@gzip_page
@response_wrapper
def get_sensitivity(request):
    return validate_get_request(request, get_sensitivity_data)

@gzip_page
@response_wrapper
def get_scalar(request):
    return validate_get_request(request, get_scalar_data)

@gzip_page
@response_wrapper
def r_control(request):
    return validate_get_request(request, get_contorl_data)

@gzip_page
@response_wrapper
def c_control(request):
    return validate_get_request(request, change_control)

@gzip_page
@response_wrapper
def parameters(request):
    return validate_get_request(request, get_parameters_data)

@gzip_page
@response_wrapper
def get_weight(request):
    return validate_get_request(request, get_weight_data)

@gzip_page
@response_wrapper
def get_weight_grad(request):
    return validate_get_request(request, get_weightGrad_data)

@gzip_page
@response_wrapper
def get_bias(request):
    return validate_get_request(request, get_bias_data)

@gzip_page
@response_wrapper
def get_bias_grad(request):
    return validate_get_request(request, get_biasGrad_data)

@gzip_page
@response_wrapper
def set_monitor(request):
    return validate_post_request(request, set_monitor_data)

@gzip_page
@response_wrapper
def set_cycle(request):
    return validate_get_request(request, set_cycle_data)

@gzip_page
@response_wrapper
def set_node_(request):
    return validate_get_request(request, set_node_data)


@gzip_page
@response_wrapper
def set_prun(request):
    return validate_post_request(request, set_prun_data)

@gzip_page
@response_wrapper
def set_playTag(request):
    return validate_get_request(request, set_playTag_data)

@gzip_page
@response_wrapper
def set_trainCycle(request):
    return validate_get_request(request, set_trainCycle_data)

@gzip_page
@response_wrapper
def set_dropout(request):
    return validate_get_request(request, set_dropout_data)

@gzip_page
@response_wrapper
def set_batchsize(request):
    return validate_get_request(request, set_batchsize_data)

@gzip_page
@response_wrapper
def set_lr(request):
    return validate_get_request(request, set_lr_data)

@gzip_page
@response_wrapper
def set_keep(request):
    return validate_get_request(request, set_keep_data)

@gzip_page
@response_wrapper
def get_traindata(request):
    return validate_get_request(request, get_trainData)

@gzip_page
@response_wrapper
def modelTxt(request):
    return validate_post_request(request, modelTxtUrlReader)

@gzip_page
@response_wrapper
def get_test(request):
    return validate_get_request(request, get_test_data)

@gzip_page
@response_wrapper
def get_automl_list(request):
    return validate_get_request(request, get_automl_list_data)

@gzip_page
@response_wrapper
def get_automl_graph(request):
    return validate_get_request(request, get_automl_graph_data)

@gzip_page
@response_wrapper
def exec_automl(request):
    return validate_get_request(request, automl_executor)


@gzip_page
@response_wrapper
def exec_roughautoml(request):
    return validate_post_request(request, roughautoml_executor)

@gzip_page
@response_wrapper
def exec_graphUrlDealer(request):
    return validate_post_request(request, graphUrlDealer)