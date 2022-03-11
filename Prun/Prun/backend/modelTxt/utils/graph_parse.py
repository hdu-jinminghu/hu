import torch
import torch.nn as nn
import numpy as np
import json

from collections import OrderedDict

from tensorboard.compat.proto.config_pb2 import RunMetadata
from tensorboard.compat.proto.graph_pb2 import GraphDef
from tensorboard.compat.proto.step_stats_pb2 import StepStats, DeviceStepStats
from tensorboard.compat.proto.versions_pb2 import VersionDef

from torch.utils.tensorboard._proto_graph import node_proto
# "aten::relu" or i.kind == "aten::relu_"
conserv = ["aten::add_", "aten::flatten","aten::view","aten::cat","aten::add","aten::to","aten::upsample_nearest2d"]
splitOp = ["aten::relu","aten::relu_","aten::max_pool2d","aten::max_pool2d_","aten::max_pool1d","aten::max_pool21_","aten::avg_pool2d","aten::avg_pool2d_",
           "aten::sigmoid","aten::sigmoid_","aten::tanh_","aten::tanh"]
methods_OP = ['attributeNames', 'hasMultipleOutputs', 'hasUses', 'inputs',
              'kind', 'outputs', 'outputsSize', 'scopeName']
# Some additional methods to explure for methods_IO are
#
#   'unique' (type int)
#   'type' (type <Tensor<class 'torch._C.Type'>>)
#
# But the below are sufficient for now.
methods_IO = ['node', 'offset', 'debugName']

GETATTR_KIND = 'prim::GetAttr'
CLASSTYPE_KIND = 'ClassType'

class NodeBase(object):
    def __init__(self, debugName=None, inputs=None, scope=None, tensor_size=None, op_type='UnSpecified', attributes=''):
        # TODO; Specify a __slots__ for this class or potentially
        # used namedtuple instead
        self.debugName = debugName
        self.inputs = inputs
        self.tensor_size = tensor_size
        self.kind = op_type
        self.attributes = attributes
        self.scope = scope

    def __repr__(self):
        repr = []
        repr.append(str(type(self)))
        for m in dir(self):
            if '__' not in m:
                repr.append(m + ': ' + str(getattr(self, m)) + str(type(getattr(self, m))))
        return '\n'.join(repr) + '\n\n'


class NodePy(NodeBase):
    def __init__(self, node_cpp, valid_methods):
        super(NodePy, self).__init__(node_cpp)
        valid_methods = valid_methods[:]
        self.inputs = []

        for m in valid_methods:
            if m == 'inputs' or m == 'outputs':
                list_of_node = list(getattr(node_cpp, m)())
                io_unique_names = []
                io_tensor_sizes = []
                for n in list_of_node:
                    io_unique_names.append(n.debugName())
                    if n.isCompleteTensor():
                        io_tensor_sizes.append(n.type().sizes())
                    else:
                        io_tensor_sizes.append(None)

                setattr(self, m, io_unique_names)
                setattr(self, m + 'tensor_size', io_tensor_sizes)

            else:
                setattr(self, m, getattr(node_cpp, m)())


class NodePyIO(NodePy):
    def __init__(self, node_cpp, input_or_output=None):
        super(NodePyIO, self).__init__(node_cpp, methods_IO)
        try:
            tensor_size = node_cpp.type().sizes()
        except RuntimeError:
            tensor_size = [1, ]  # fail when constant model is used.
        self.tensor_size = tensor_size
        # Kind attribute string is purely descriptive and will be shown
        # in detailed information for the node in TensorBoard's graph plugin.
        #
        # NodePyOP nodes get this from their kind() method.
        self.kind = 'Parameter'
        if input_or_output:
            self.input_or_output = input_or_output
            self.kind = 'IO Node'


class NodePyOP(NodePy):
    def __init__(self, node_cpp):
        super(NodePyOP, self).__init__(node_cpp, methods_OP)
        # Replace single quote which causes strange behavior in TensorBoard
        # TODO: See if we can remove this in the future
        self.attributes = str({k: node_cpp[k] for k in node_cpp.attributeNames()}).replace("'", ' ')
        self.kind = node_cpp.kind()


class GraphPy(object):
    """Helper class to convert torch.nn.Module to GraphDef proto and visualization
    with TensorBoard.

    GraphDef generation operates in two passes:

    In the first pass, all nodes are read and saved to two lists.
    One list is for input/output nodes (nodes_io), which only have inbound
    or outbound connections, but not both. Another list is for internal
    operator nodes (nodes_op). The first pass also saves all scope name
    appeared in the nodes in scope_name_appeared list for later processing.

    In the second pass, scope names are fully applied to all nodes.
    debugNameToScopedName is a mapping from a node's ID to its fully qualified
    scope name. e.g. Net1/Linear[0]/1. Unfortunately torch.jit doesn't have
    totally correct scope output, so this is nontrivial. The function
    populate_namespace_from_OP_to_IO and find_common_root are used to
    assign scope name to a node based on the connection between nodes
    in a heuristic kind of way. Bookkeeping is done with shallowest_scope_name
    and scope_name_appeared.
    """
    def __init__(self):
        self.nodes_op = []
        self.nodes_io = OrderedDict()
        self.unique_name_to_scoped_name = {}
        self.shallowest_scope_name = 'default'
        self.scope_name_appeared = []

    def append(self, x):
        if isinstance(x, NodePyIO):
            self.nodes_io[x.debugName] = x
        if isinstance(x, NodePyOP):
            self.nodes_op.append(x)

    def printall(self):
        print('all nodes')
        for node in self.nodes_op:
            print(node)
        for key in self.nodes_io:
            print(self.nodes_io[key])

    def find_common_root(self):
        for fullscope in self.scope_name_appeared:
            if fullscope:
                self.shallowest_scope_name = fullscope.split('/')[0]

    def populate_namespace_from_OP_to_IO(self):
        for node in self.nodes_op:
            for node_output, outputSize in zip(node.outputs, node.outputstensor_size):
                self.scope_name_appeared.append(node.scopeName)
                self.nodes_io[node_output] = NodeBase(node_output,
                                                      node.inputs,
                                                      node.scopeName,
                                                      outputSize,
                                                      op_type=node.kind,
                                                      attributes=node.attributes)

        self.find_common_root()

        for node in self.nodes_op:
            for input_node_id in node.inputs:
                self.unique_name_to_scoped_name[input_node_id] = node.scopeName + '/' + input_node_id

        for key, node in self.nodes_io.items():
            if type(node) == NodeBase:
                self.unique_name_to_scoped_name[key] = node.scope + '/' + node.debugName
            if hasattr(node, 'input_or_output'):
                self.unique_name_to_scoped_name[key] = node.input_or_output + '/' + node.debugName

            if hasattr(node, 'scope') and node.scope is not None:
                self.unique_name_to_scoped_name[key] = node.scope + '/' + node.debugName
                if node.scope == '' and self.shallowest_scope_name:
                    self.unique_name_to_scoped_name[node.debugName] = self.shallowest_scope_name + '/' + node.debugName

        # replace name
        for key, node in self.nodes_io.items():
            self.nodes_io[key].inputs = [self.unique_name_to_scoped_name[node_input_id] for node_input_id in node.inputs]
            if node.debugName in self.unique_name_to_scoped_name:
                self.nodes_io[key].debugName = self.unique_name_to_scoped_name[node.debugName]

    def to_proto(self):
        """
        Converts graph representation of GraphPy object to TensorBoard
        required format.
        """
        # TODO: compute correct memory usage and CPU time once
        # PyTorch supports it
        nodes = []
        for v in self.nodes_io.values():
            nodes.append(node_proto(v.debugName,
                                    input=v.inputs,
                                    outputsize=v.tensor_size,
                                    op=v.kind,
                                    attributes=v.attributes))
        return nodes


def parse(graph, trace, args=None, omit_useless_nodes=True):
    """This method parses an optimized PyTorch model graph and produces
    a list of nodes and node stats for eventual conversion to TensorBoard
    protobuf format.

    Args:
      graph (PyTorch module): The model graph to be parsed.
      trace (PyTorch JIT TracedModule): The model trace to be parsed.
      args (tuple): input tensor[s] for the model.
      omit_useless_nodes (boolean): Whether to remove nodes from the graph.
    """
    n_inputs = len(args)

    scope = {}
    nodes_py = GraphPy()
    for node in graph.inputs():
        if omit_useless_nodes:
            if len(node.uses()) == 0:  # number of user of the node (= number of outputs/ fanout)
                continue

        if node.type().kind() != CLASSTYPE_KIND:
            nodes_py.append(NodePyIO(node, 'input'))

    attr_to_scope = dict()
    for node in graph.nodes():
        if node.kind() == GETATTR_KIND:
            attr_name = node.s('name')
            parent = node.input().node()
            if parent.kind() == GETATTR_KIND:  # If the parent node is not the top-level "self" node
                parent_attr_name = parent.s('name')
                parent_scope = attr_to_scope[parent_attr_name]
                attr_scope = parent_scope.split('/')[-1]
                attr_to_scope[attr_name] = '{}/{}.{}'.format(parent_scope, attr_scope, attr_name)
            else:
                attr_to_scope[attr_name] = '__module.{}'.format(attr_name)
            # We don't need classtype nodes; scope will provide this information
            if node.output().type().kind() != CLASSTYPE_KIND:
                node_py = NodePyOP(node)
                node_py.scopeName = attr_to_scope[attr_name]
                nodes_py.append(node_py)
        else:
            nodes_py.append(NodePyOP(node))

    for i, node in enumerate(graph.outputs()):  # Create sink nodes for output ops
        node_py = NodePyIO(node, 'output')
        node_py.debugName = "output.{}".format(i + 1)
        node_py.inputs = [node.debugName()]
        nodes_py.append(node_py)

    def parse_traced_name(module):
        if isinstance(module, torch.jit.TracedModule):
            module_name = module._name
        else:
            module_name = getattr(module, 'original_name', "Module")
        return module_name

    alias_to_name = dict()
    base_name = parse_traced_name(trace)
    for name, module in trace.named_modules(prefix='__module'):
        mod_name = parse_traced_name(module)
        attr_name = name.split('.')[-1]
        alias_to_name[name] = '{}[{}]'.format(mod_name, attr_name)

    for node in nodes_py.nodes_op:
        module_aliases = node.scopeName.split('/')
        replacements = [
            alias_to_name[alias]
            if alias in alias_to_name
            else alias.split('.')[-1]
            for alias in module_aliases
        ]
        node.scopeName = base_name
        if any(replacements):
            node.scopeName += '/' + '/'.join(replacements)
            
    # print(nodes_py.nodes_io)
    # 节点映射：输入输出
    relu = {}
    id_map = {}
    for i in nodes_py.nodes_io:
        id_map[i] = nodes_py.nodes_io[i].input_or_output
    drop = []
    # 节点映射：操作
    for i in nodes_py.nodes_op:
        # if i.kind == "aten::add":
        #     print(i)
        # print(i)
        debugName = str(i.debugName)
        
        scope = i.scopeName
        # lstm模块打包成一个
        # if 'scope: __module.lstm' in debugName or 'scope: __module.rnn' in debugName or 'scope: __module.gru' in debugName:
        if r'torch\nn\modules\rnn.py' in debugName or r'torch\nn\modules\lstm.py' in debugName or r'torch\nn\modules\gru.py' in debugName:
            
            nameContent = debugName.split("=")[0]
            ids = nameContent.split("%")
            for id_ in ids[1:]:
                id_ = id_.split(" :")[0]
                id_map[id_] = scope
            continue
        
        if i.kind == "prim::TupleUnpack":
            nameContent = debugName.split("=")[0]
            ids = nameContent.split("%")
            for id_ in ids[1:]:
                id_ = id_.split(" :")[0]
                id_map[id_] = scope + "/" + id_
            continue
        
        debugNameList = debugName.split(" ")
        id_ = debugNameList[0][1:]
        
        
        # 有name的是weight、bias
        if "name" in i.attributes or i.kind == "aten::size":
            drop.append(id_)
            continue

        # flatten只有第一个有用
        if "flatten" in debugName:
            drop.append(i.inputs[1])
            drop.append(i.inputs[2])
        # 全连接层转置操作
        if i.kind == "aten::t" or i.kind == "prim::NumToTensor":
            drop.append(id_)
        
        if i.kind in conserv:
            scope = scope + "/" + id_
        elif id_.isdigit() and i.kind !="aten::addmm":
            for input_size in i.inputstensor_size:
                if input_size != None:
                    scope = scope + "/" + id_
                    break
        if i.kind == "aten::matmul":
            scopeName = str(i.scopeName)
            scopeNameList = scopeName.split("/")
            if "Linear" in scopeNameList[-1]:
                scope = str(i.scopeName)
 
        if i.kind in splitOp:
            # print(i)
            scopeName = str(i.scopeName)
            if scopeName in relu:
                scopeN = relu[scopeName]
                relu[scopeName] = relu[scopeName] + 1
                scope = "{}({})".format(scopeName,scopeN)
            else:
                relu[scopeName] = 1
                scope = "{}(0)".format(scopeName)

        id_map[id_] = scope

        
    #     if id_ == "h_t.1":
    #         print(i)
    # # print(id_map)
    # 构建网络
    struct = {}
    for i in nodes_py.nodes_io:
        id_ = nodes_py.nodes_io[i].input_or_output
        struct[id_] = {}
        struct[id_]["inputs"] = set()
        struct[id_]["op"] = "aten::io"
        struct[id_]["name"] = id_
        for input in nodes_py.nodes_io[i].inputs:
            struct[id_]["inputs"].add(id_map[input])
            
    for i in nodes_py.nodes_op:
        # print
        debugName = str(i.debugName)
        debugNameList = debugName.split(" ")
        id_ = debugNameList[0][1:]
        scope = str(i.scopeName)
        tag = True
        # flatten,view的id_均为input
        if i.kind in conserv:
            scope = scope + "/" + id_
            tag = False
        
        # lstm层
        # if 'scope: __module.lstm' in debugName or 'scope: __module.rnn' in debugName or 'scope: __module.gru' in debugName:
        if r'torch\nn\modules\rnn.py' in debugName or r'torch\nn\modules\lstm.py' in debugName or r'torch\nn\modules\gru.py' in debugName:
            if scope not in struct.keys():
                struct[scope] = {}
                if 'scope: __module.lstm' in debugName:
                    struct[scope]["op"] = "lstm"
                if 'scope: __module.rnn' in debugName:
                    struct[scope]["op"] = "rnn"
                if 'scope: __module.gru' in debugName:
                    struct[scope]["op"] = "gru"
                
                struct[scope]["name"] = scope
                struct[scope]["inputs"] = set()
            for input,size in zip(i.inputs,i.inputstensor_size):
                if i.kind == "aten::cat":
                    struct[scope]["inputs"].add(id_map[input])
                if size == None:
                    continue
                if input in drop:
                    continue
                struct[scope]["inputs"].add(id_map[input])
            continue
        # 解包独立处理
        if i.kind == "prim::TupleUnpack":
            nameContent = debugName.split("=")[0]
            ids = nameContent.split("%")
            for id_ in ids[1:]:
                id_ = id_.split(" :")[0]
                scope_ = scope+'/'+id_
                struct[scope_] = {}
                struct[scope_]['name'] = scope_
                struct[scope_]['op'] = 'TupleUnpack'
                struct[scope_]["inputs"] = set()
                for input in i.inputs:
                    struct[scope_]["inputs"].add(id_map[input])
            continue
        
        if i.kind == "aten::add":
            struct[scope] = {}
            struct[scope]['name'] = scope
            struct[scope]['op'] = "add"
            struct[scope]["inputs"] = set()
            for input in range(2):
                if input in id_map:
                    struct[scope]["inputs"].add(id_map[input])
                
        # 矩阵接连操作，只能通过输入识别
        elif id_.isdigit() and i.kind !="aten::addmm" and i.kind not in conserv:
            for input_size in i.inputstensor_size:
                if input_size != None:
                    scope = scope + "/" + id_
                    tag = False
                    break
        # !============
        if i.kind == "aten::matmul":
            scopeName = str(i.scopeName)
            scopeNameList = scopeName.split("/")
            if "Linear" in scopeNameList[-1]:
                scope = str(i.scopeName)
        # !============
        node = {}
        if i.kind =="aten::Int":
            continue
        # 全连接层操作是例外，debugname是数字
        if id_.isdigit() and i.kind !="aten::addmm" and tag:
            continue
        if id_ in drop:
            continue
        # relu层分离
        if i.kind in splitOp:
            scope = id_map[id_]
        if scope in struct.keys():
            for input,size in zip(i.inputs,i.inputstensor_size):
                if size == None:
                    continue
                if input in drop:
                    continue
                struct[scope]["inputs"].add(id_map[input])       
        else:
            struct[scope] = {}
            struct[scope]["inputs"] = set()
            for input,size in zip(i.inputs,i.inputstensor_size):
                if i.kind == "aten::cat":
                    struct[scope]["inputs"].add(id_map[input])
                if size == None:
                    continue
                if input in drop:
                    continue
                struct[scope]["inputs"].add(id_map[input])
                
            if i.kind == "aten::matmul":
                scopeName = str(i.scopeName)
                scopeNameList = scopeName.split("/")
                if "Linear" in scopeNameList[-1]:
                    struct[scope]["op"] = "linear"
                else:
                    struct[scope]["op"] = "linear" if i.kind == "aten::addmm" else i.kind[6:]
            else:
                struct[scope]["op"] = "linear" if i.kind == "aten::addmm" else i.kind[6:]
            struct[scope]["name"] = scope
        
        
    delList = []
    for i in struct:
        if len(struct[i]["inputs"]) == 0 and struct[i]['op'] == 'mul':
            delList.append(i)
            continue
        if "input" in i:
            lists = i.split("/")
            parent = "/".join(lists[:-1])
            struct[i]["inputs"] = struct[i]["inputs"] - set([parent])
        struct[i]["inputs"] = list(struct[i]["inputs"] - set([i]))
    for i in delList:
        del struct[i]
    # with open("C:\\Users\\nuoya\\Desktop\\t.json","w") as f:
    #     json.dump(struct,f) 
    # nodes_py.populate_namespace_from_OP_to_IO()
    # return nodes_py.to_proto()
    # print(struct)
    
    layers = list(struct.keys())
    inputs = []
    for layer in layers:
        inputs.extend(struct[layer]["inputs"])
    
    for layer in layers:
        if (not layer in inputs) and (layer != "output"):
            del struct[layer]
    
    return struct