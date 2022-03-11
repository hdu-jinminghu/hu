class Commad():
    def execute(self,net, config,skip_vertex_list):
        raise Exception("execute函数")
# fixed固定网络层
class ValidateFixLayer(Commad):
    def execute(self, net, config,skip_vertex_list):
        fixed,limitations,depth = config["fixed"],config["limitations"],config["depth"]
        layers = list(net.keys())
        for fixed_layer in fixed:
            if not fixed_layer in layers:
                return False
        return True
# 网络深度
class ValidateDepth(Commad):
    def execute(self, net, config,skip_vertex_list):
        fixed,limitations,depth = config["fixed"],config["limitations"],config["depth"]
        layers = list(net.keys())
        main_flow = []
        for layer in layers:
            if (not layer in skip_vertex_list) and (not net[layer]["type"].startswith("op")):
                main_flow.append(layer)
        if len(main_flow)<depth[0] or len(main_flow)>depth[1]:
            return False
        return True

# 网络层间隔深度
class ValidateLayerGap(Commad):
    def execute(self, net, config,skip_vertex_list):
        fixed,limitations,depth = config["fixed"],config["limitations"],config["depth"] 
        layers = list(net.keys())
        main_flow = []
        for layer in layers:
            if (not layer in skip_vertex_list) and (not net[layer]["type"].startswith("op")):
                main_flow.append(layer)
        for limitation in limitations:
            head_index = main_flow.index(limitation[0])
            tail_index = main_flow.index(limitation[1])
            
            gap = abs(head_index-tail_index) - 1
            if gap<limitation[2] or gap>limitation[3]:
                return False
        return True



class Validator():
    def __init__(self):
        self.rule_list = []
        
    def add_rule(self, rule):
        self.rule_list.append(rule)
        return self
        
    def execute(self, net, config,skip_vertex_list):
        res = True
        for rule in self.rule_list:
            res = res & rule.execute(net, config,skip_vertex_list)
            if not res:
                return res
        return res