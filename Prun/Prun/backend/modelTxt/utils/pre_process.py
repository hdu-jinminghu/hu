
import torch
import torch.nn as nn
import numpy as np
import json
# from .utils import graph_parse
from .graph_parse import parse
from ptflops import get_model_complexity_info
type_ = {"nn.BatchNorm2d":"bn","nn.Linear":"linear","nn.Conv2d":"conv","nn.BatchNorm1d":"bn","nn.Conv1d":"conv"}

dropout = "nn.Dropout"
# 保存模型特征：type_ 和 kernelSize
# utils.kernel_size(solver.model)
def kernel_size(model = None, path = ".", name = 0):
    dics = {}
    json_path = path + "/kernel_size.json"
    for name,module__ in model.named_modules():
        if not name:
            continue
        id_ = name.split(".")
        module = 'model'
        for i in id_:
            module_ = "._modules['{}']".format(i)
            module = module + module_
        mod = eval(module)
        # if isinstance(mod,nn.LSTM):
        #     for i in mod.named_parameters():
        #         print(i[0],i[1].shape)
        for instance in type_.keys():
            if isinstance(mod,eval(instance)):
                dics[name] = {}
                torch_shape = str(mod.weight.shape)
                shape = torch_shape[11:-1]
                dics[name]["shape"] = shape
                dics[name]["type"] = type_[instance]
        if isinstance(mod,nn.Dropout):
            dics[name] = {}
            dics[name]["type"] = "dropout"
            dics[name]["shape"] = str(mod.p)
        if isinstance(mod,nn.ReLU):
            dics[name] = {}
            dics[name]["type"] = "relu"
    with open(json_path,"w") as f:
        json.dump(dics, f)

# 保存模型结构
# utils.model_structure(solver.model,torch.rand([1, 3, 32, 32]).to("cuda"))
def model_structure(model = None, args = None, path = ".", name = 0):
    json_path = path + "/structure.json"
    
    with torch.onnx.select_model_mode_for_export(model, torch.onnx.TrainingMode.EVAL):  # TODO: move outside of torch.onnx?
        try:
            trace = torch.jit.trace(model, args)
            graph = trace.graph
            torch._C._jit_pass_inline(graph)
        except RuntimeError as e:
            print(e)
            print('Error occurs, No graph saved')
            raise e
    struct = parse(graph, trace, args)
    with open(json_path,"w") as f:
        json.dump(struct, f)


def get_model_info(model = None, input_size = None, path = None, name = 0):
    json_path = path + "/parameters.json"
    with torch.cuda.device(0):
        macs, params = get_model_complexity_info(model, input_size, as_strings=True,
                                                print_per_layer_stat=True, verbose=True)
        # with open(json_path,"w") as f:
        #     json.dump({"GMac":macs,"size":params}, f)