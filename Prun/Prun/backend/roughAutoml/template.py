# LEVEL_0 = [{"type":"conv2d","attr":{"padding":1,"bias":True,"stride":1,"in_channels":None,"out_channels":None,"kernel_size":3}},
#            {"type":"conv2d","attr":{"padding":0,"bias":True,"stride":1,"in_channels":None,"out_channels":None,"kernel_size":1}},
#            {"type":"maxpool2d","attr":{"padding":1,"stride":1,"kernel_size":3}},
#            {"type":"avgpool2d","attr":{"padding":1,"stride":1,"kernel_size":3}},
#            {"type":"identity","attr":{}},]


LEVEL_0 = [
    # 3*3 conv +bn +relu
    {'lineList': [{'Remark': '', 'from': 'vertexa0', 'to': 'vertexa1', 'label': '连线名称', 'id': 'vertexa0-vertexa1'}, {'Remark': '', 'from': 'vertexa1', 'to': 'vertexa2', 'label': '连线名称', 'id': 'vertexa1-vertexa2'}, 
                  {'Remark': '', 'from': 'vertexa2', 'to': 'vertexa3', 'label': '连线名称', 'id': 'vertexa2-vertexa3'}, {'Remark': '', 'from': 'vertexa3', 'to': 'vertexa4', 'label': '连线名称', 'id': 'vertexa3-vertexa4'}], 
    'nodeList': [{'attrs': {}, 'type': 'input', 'id': 'vertexa0', 'nodeName': 'input', 'typeName': 'input', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                 {'attrs': {'padding': 1, 'bias': True, 'stride': 1, 'in_channels': None, 'out_channels': None, 'kernel_size': 3}, 'type': 'conv2d', 'id': 'vertexa1', 'nodeName': 'conv2d', 'typeName': 'conv2d', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                 {'attrs': {'num_features': None}, 'type': 'bn2d', 'id': 'vertexa2', 'nodeName': 'bn2d', 'typeName': 'bn2d', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, {'attrs': {'inplace': True}, 'type': 'relu', 'id': 'vertexa3', 'nodeName': 'relu', 'typeName': 'relu', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                 {'attrs': {}, 'type': 'output', 'id': 'vertexa4', 'nodeName': 'output', 'typeName': 'output', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}]},
    # 1*1 conv
    {'lineList': [{'Remark': '', 'from': 'vertexa0', 'to': 'vertexa1', 'label': '连线名称', 'id': 'vertexa0-vertexa1'}, {'Remark': '', 'from': 'vertexa1', 'to': 'vertexa2', 'label': '连线名称', 'id': 'vertexa1-vertexa2'}], 
     'nodeList': [{'attrs': {}, 'type': 'input', 'id': 'vertexa0', 'nodeName': 'input', 'typeName': 'input', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {'padding': 0, 'bias': True, 'stride': 1, 'in_channels': None, 'out_channels': None, 'kernel_size': 1}, 'type': 'conv2d', 'id': 'vertexa1', 'nodeName': 'conv2d', 'typeName': 'conv2d', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {}, 'type': 'output', 'id': 'vertexa2', 'nodeName': 'output', 'typeName': 'output', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}]},
    # maxpool
    {'lineList': [{'Remark': '', 'from': 'vertexa0', 'to': 'vertexa1', 'label': '连线名称', 'id': 'vertexa0-vertexa1'}, {'Remark': '', 'from': 'vertexa1', 'to': 'vertexa2', 'label': '连线名称', 'id': 'vertexa1-vertexa2'}], 
     'nodeList': [{'attrs': {}, 'type': 'input', 'id': 'vertexa0', 'nodeName': 'input', 'typeName': 'input', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {'padding': 1, 'stride': 1, 'kernel_size': 3}, 'type': 'maxpool2d', 'id': 'vertexa1', 'nodeName': 'maxpool2d', 'typeName': 'maxpool2d', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {}, 'type': 'output', 'id': 'vertexa2', 'nodeName': 'output', 'typeName': 'output', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}]},
    # avepool
    {'lineList': [{'Remark': '', 'from': 'vertexa0', 'to': 'vertexa1', 'label': '连线名称', 'id': 'vertexa0-vertexa1'}, {'Remark': '', 'from': 'vertexa1', 'to': 'vertexa2', 'label': '连线名称', 'id': 'vertexa1-vertexa2'}], 
     'nodeList': [{'attrs': {}, 'type': 'input', 'id': 'vertexa0', 'nodeName': 'input', 'typeName': 'input', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {'padding': 1, 'stride': 1, 'kernel_size': 3}, 'type': 'avgpool2d', 'id': 'vertexa1', 'nodeName': 'avgpool2d', 'typeName': 'avgpool2d', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {}, 'type': 'output', 'id': 'vertexa2', 'nodeName': 'output', 'typeName': 'output', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}]},
    # sequence
    # {'lineList': [{'Remark': '', 'from': 'vertexa0', 'to': 'vertexa1', 'label': '连线名称', 'id': 'vertexa0-vertexa1'}, {'Remark': '', 'from': 'vertexa1', 'to': 'vertexa2', 'label': '连线名称', 'id': 'vertexa1-vertexa2'}], 
    #  'nodeList': [{'attrs': {}, 'type': 'input', 'id': 'vertexa0', 'nodeName': 'input', 'typeName': 'input', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
    #               {'attrs': {}, 'type': 'sequence', 'id': 'vertexa1', 'nodeName': 'sequence', 'typeName': 'sequence', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
    #               {'attrs': {}, 'type': 'output', 'id': 'vertexa2', 'nodeName': 'output', 'typeName': 'output', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}]},
    
]

# 基础操作存在pool,cat不能使用
LEVEL_1 = [
    # 0 -> 1 -> 2 -> 3 ->4 
    {'lineList': [{'Remark': '', 'from': 'vertexb0', 'to': 'vertexb1', 'label': '连线名称', 'id': 'vertexb0-vertexb1'}, {'Remark': '', 'from': 'vertexb1', 'to': 'vertexb2', 'label': '连线名称', 'id': 'vertexb1-vertexb2'}, 
                  {'Remark': '', 'from': 'vertexb2', 'to': 'vertexb3', 'label': '连线名称', 'id': 'vertexb2-vertexb3'}, {'Remark': '', 'from': 'vertexb3', 'to': 'vertexb4', 'label': '连线名称', 'id': 'vertexb3-vertexb4'}], 
     'nodeList': [{'attrs': {}, 'type': 'input', 'id': 'vertexb0', 'nodeName': 'input', 'typeName': 'input', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, {'attrs': {}, 'type': 'level0[0]', 'id': 'vertexb1', 'nodeName': 'level0[0]', 'typeName': 'level0[0]', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {}, 'type': 'level0[0]', 'id': 'vertexb2', 'nodeName': 'level0[0]', 'typeName': 'level0[0]', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, {'attrs': {}, 'type': 'level0[0]', 'id': 'vertexb3', 'nodeName': 'level0[0]', 'typeName': 'level0[0]', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {}, 'type': 'output', 'id': 'vertexb4', 'nodeName': 'output', 'typeName': 'output', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}]},
    #   ->      3
    # 0 -> 1 -> 2 -> add -> 5
    {'lineList': [{'Remark': '', 'from': 'vertexb0', 'to': 'vertexb1', 'label': '连线名称', 'id': 'vertexb0-vertexb1'}, {'Remark': '', 'from': 'vertexb0', 'to': 'vertexb3', 'label': '连线名称', 'id': 'vertexb0-vertexb3'}, {'Remark': '', 'from': 'vertexb1', 'to': 'vertexb2', 'label': '连线名称', 'id': 'vertexb1-vertexb2'}, {'Remark': '', 'from': 'vertexb2', 'to': 'vertexb4', 'label': '连线名称', 'id': 'vertexb2-vertexb4'}, 
                  {'Remark': '', 'from': 'vertexb3', 'to': 'vertexb4', 'label': '连线名称', 'id': 'vertexb3-vertexb4'}, {'Remark': '', 'from': 'vertexb4', 'to': 'vertexb5', 'label': '连线名称', 'id': 'vertexb4-vertexb5'}], 
     'nodeList': [{'attrs': {}, 'type': 'input', 'id': 'vertexb0', 'nodeName': 'input', 'typeName': 'input', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, {'attrs': {}, 'type': 'level0[0]', 'id': 'vertexb1', 'nodeName': 'level0[0]', 'typeName': 'level0[0]', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {}, 'type': 'level0[0]', 'id': 'vertexb2', 'nodeName': 'level0[0]', 'typeName': 'level0[0]', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, {'attrs': {}, 'type': 'level0[0]', 'id': 'vertexb3', 'nodeName': 'level0[0]', 'typeName': 'level0[0]', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {}, 'type': 'op_add', 'id': 'vertexb4', 'nodeName': 'op_add', 'typeName': 'op_add', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, {'attrs': {}, 'type': 'output', 'id': 'vertexb5', 'nodeName': 'output', 'typeName': 'output', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}]},
    #        -> 2
    # 0 -> 1 -> 3 -> add -> 6
    #        -> 4 
    {'lineList': [{'Remark': '', 'from': 'vertexb0', 'to': 'vertexb1', 'label': '连线名称', 'id': 'vertexb0-vertexb1'}, {'Remark': '', 'from': 'vertexb1', 'to': 'vertexb2', 'label': '连线名称', 'id': 'vertexb1-vertexb2'}, {'Remark': '', 'from': 'vertexb1', 'to': 'vertexb3', 'label': '连线名称', 'id': 'vertexb1-vertexb3'}, 
                  {'Remark': '', 'from': 'vertexb1', 'to': 'vertexb4', 'label': '连线名称', 'id': 'vertexb1-vertexb4'}, {'Remark': '', 'from': 'vertexb2', 'to': 'vertexb5', 'label': '连线名 称', 'id': 'vertexb2-vertexb5'}, {'Remark': '', 'from': 'vertexb3', 'to': 'vertexb5', 'label': '连线名称', 'id': 'vertexb3-vertexb5'}, 
                  {'Remark': '', 'from': 'vertexb4', 'to': 'vertexb5', 'label': '连线名称', 'id': 'vertexb4-vertexb5'}, {'Remark': '', 'from': 'vertexb5', 'to': 'vertexb6', 'label': '连线名称', 'id': 'vertexb5-vertexb6'}], 
     'nodeList': [{'attrs': {}, 'type': 'input', 'id': 'vertexb0', 'nodeName': 'input', 'typeName': 'input', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, {'attrs': {}, 'type': 'level0[0]', 'id': 'vertexb1', 'nodeName': 'level0[0]', 'typeName': 'level0[0]', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {}, 'type': 'level0[0]', 'id': 'vertexb2', 'nodeName': 'level0[0]', 'typeName': 'level0[0]', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, {'attrs': {}, 'type': 'level0[0]', 'id': 'vertexb3', 'nodeName': 'level0[0]', 'typeName': 'level0[0]', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {}, 'type': 'level0[0]', 'id': 'vertexb4', 'nodeName': 'level0[0]', 'typeName': 'level0[0]', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, {'attrs': {}, 'type': 'op_add', 'id': 'vertexb5', 'nodeName': 'op_add', 'typeName': 'op_add', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {}, 'type': 'output', 'id': 'vertexb6', 'nodeName': 'output', 'typeName': 'output', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}]},
    # 0 -> 1 -> 2 -> 5 -> 6
    #   -> 3 -> 4 
    # {'lineList': [{'Remark': '', 'from': 'vertex0', 'to': 'vertex1', 'label': '连线名称', 'id': 'vertex0-vertex1'}, {'Remark': '', 'from': 'vertex0', 'to': 'vertex3', 'label': '连线名称', 'id': 'vertex0-vertex3'}, {'Remark': '', 'from': 'vertex1', 'to': 'vertex2', 'label': '连线名称', 'id': 'vertex1-vertex2'}, 
    #               {'Remark': '', 'from': 'vertex2', 'to': 'vertex5', 'label': '连线名称', 'id': 'vertex2-vertex5'}, {'Remark': '', 'from': 'vertex3', 'to': 'vertex4', 'label': '连线名称', 'id': 'vertex3-vertex4'}, {'Remark': '', 'from': 'vertex4', 'to': 'vertex5', 'label': '连线名称', 'id': 'vertex4-vertex5'}, 
    #               {'Remark': '', 'from': 'vertex5', 'to': 'vertex6', 'label': '连线名称', 'id': 'vertex5-vertex6'}], 
    #  'nodeList': [{'attrs': {}, 'type': 'input', 'id': 'vertex0', 'nodeName': 'input', 'typeName': 'input', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, {'attrs': {}, 'type': 'module1', 'id': 'vertex1', 'nodeName': 'module1', 'typeName': 'module1', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
    #               {'attrs': {}, 'type': 'module1', 'id': 'vertex2', 'nodeName': 'module1', 'typeName': 'module1', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, {'attrs': {}, 'type': 'module1', 'id': 'vertex3', 'nodeName': 'module1', 'typeName': 'module1', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
    #               {'attrs': {}, 'type': 'module1', 'id': 'vertex4', 'nodeName': 'module1', 'typeName': 'module1', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, {'attrs': {}, 'type': 'op_add', 'id': 'vertex5', 'nodeName': 'op_add', 'typeName': 'op_add', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
    #               {'attrs': {}, 'type': 'output', 'id': 'vertex6', 'nodeName': 'output', 'typeName': 'output', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}]}
    
    # 直连
    {'lineList': [{'Remark': '', 'from': 'vertexb0', 'to': 'vertexb1', 'label': '连线名称', 'id': 'vertexb0-vertexb1'}, {'Remark': '', 'from': 'vertexb1', 'to': 'vertexb2', 'label': '连线名称', 'id': 'vertexb1-vertexb2'}], 
     'nodeList': [{'attrs': {}, 'type': 'input', 'id': 'vertexb0', 'nodeName': 'input', 'typeName': 'input', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {}, 'type': 'sequence', 'id': 'vertexb1', 'nodeName': 'sequence', 'typeName': 'sequence', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
                  {'attrs': {}, 'type': 'output', 'id': 'vertexb2', 'nodeName': 'output', 'typeName': 'output', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}]},
]

# testGraph = {'lineList': [{'Remark': '', 'from': 'vertex0', 'to': 'vertex1', 'label': '连线名称', 'id': 'vertex0-vertex1'}, 
#                 {'Remark': '', 'from': 'vertex1', 'to': 'vertex2', 'label': '连线名称', 'id': 'vertex1-vertex2'}, 
#                 {'Remark': '', 'from': 'vertex2', 'to': 'vertex3', 'label': '连线名称', 'id': 'vertex2-vertex3'}, 
#                 {'Remark': '', 'from': 'vertex3', 'to': 'vertex4', 'label': '连线名称', 'id': 'vertex3-vertex4'}, 
#                 {'Remark': '', 'from': 'vertex4', 'to': 'vertex5', 'label': '连线名 称', 'id': 'vertex4-vertex5'}, 
#                 {'Remark': '', 'from': 'vertex5', 'to': 'vertex6', 'label': '连线名称', 'id': 'vertex5-vertex6'}, 
#                 {'Remark': '', 'from': 'vertex6', 'to': 'vertex7', 'label': '连线名称', 'id': 'vertex6-vertex7'}, 
#                 {'Remark': '', 'from': 'vertex7', 'to': 'vertex8', 'label': '连线名称', 'id': 'vertex7-vertex8'}, 
#                 {'Remark': '', 'from': 'vertex8', 'to': 'vertex9', 'label': '连线名称', 'id': 'vertex8-vertex9'}], 
#             'nodeList': [{'attrs': {}, 'type': 'input', 'id': 'vertex0', 'nodeName': 'input', 'typeName': 'input', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
#                  {'attrs': {}, 'type': 'module1', 'id': 'vertex1', 'nodeName': 'module1', 'typeName': 'module1', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
#                  {'attrs': {}, 'type': 'module1', 'id': 'vertex2', 'nodeName': 'module1', 'typeName': 'module1', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
#                  {'attrs': {'padding': 1, 'bias': True, 'stride': 1, 'in_channels': 32, 'out_channels': 64, 'kernel_size': 3}, 'type': 'conv2d', 'id': 'vertex3', 'nodeName': 'conv2d', 'typeName': 'conv2d', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
#                  {'attrs': {}, 'type': 'module2', 'id': 'vertex4', 'nodeName': 'module2', 'typeName': 'module2', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
#                  {'attrs': {}, 'type': 'module2', 'id': 'vertex5', 'nodeName': 'module2', 'typeName': 'module2', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
#                  {'attrs': {}, 'type': 'adaptiveavgpool2d', 'id': 'vertex6', 'nodeName': 'adaptiveavgpool2d', 'typeName': 'adaptiveavgpool2d', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
#                  {'attrs': {}, 'type': 'op_view', 'id': 'vertex7', 'nodeName': 'op_view', 'typeName': 'op_view', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
#                  {'attrs': {'in_features': 64, 'out_features': 10, 'bias': True}, 'type': 'linear', 'id': 'vertex8', 'nodeName': 'linear', 'typeName': 'linear', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}, 
#                  {'attrs': {}, 'type': 'output', 'id': 'vertex9', 'nodeName': 'output', 'typeName': 'output', 'log_bg_color': 'rgba(250, 205, 81, 0.2)'}]
# }

# holderPlace = [{"channels":32,"deepth":10,"type":"module1"},
#                {"channels":64,"deepth":5,"type":"module2"}]