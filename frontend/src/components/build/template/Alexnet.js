const Alexnetgraph = {
    "lineList":[
        {
            "Remark":"",
            "from":"Alexnet1",
            "to":"Alexnet2",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet1-Alexnet2"
        },
        {
            "Remark":"",
            "from":"Alexnet2",
            "to":"Alexnet3",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet2-Alexnet3"
        },
        {
            "Remark":"",
            "from":"Alexnet3",
            "to":"Alexnet4",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet3-Alexnet4"
        },
        {
            "Remark":"",
            "from":"Alexnet4",
            "to":"Alexnet5",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet4-Alexnet5"
        },
        {
            "Remark":"",
            "from":"Alexnet5",
            "to":"Alexnet6",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet5-Alexnet6"
        },
        {
            "Remark":"",
            "from":"Alexnet6",
            "to":"Alexnet7",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet6-Alexnet7"
        },
        {
            "Remark":"",
            "from":"Alexnet7",
            "to":"Alexnet8",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet7-Alexnet8"
        },
        {
            "Remark":"",
            "from":"Alexnet8",
            "to":"Alexnet9",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet8-Alexnet9"
        },
        {
            "Remark":"",
            "from":"Alexnet9",
            "to":"Alexnet10",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet9-Alexnet10"
        },
        {
            "Remark":"",
            "from":"Alexnet10",
            "to":"Alexnet11",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet10-Alexnet11"
        },
        {
            "Remark":"",
            "from":"Alexnet11",
            "to":"Alexnet12",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet11-Alexnet12"
        },
        {
            "Remark":"",
            "from":"Alexnet12",
            "to":"Alexnet13",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet12-Alexnet13"
        },
        {
            "Remark":"",
            "from":"Alexnet13",
            "to":"Alexnet14",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet13-Alexnet14"
        },
        {
            "Remark":"",
            "from":"Alexnet14",
            "to":"Alexnet15",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet14-Alexnet15"
        },
        {
            "Remark":"",
            "from":"Alexnet15",
            "to":"Alexnet16",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet15-Alexnet16"
        },
        {
            "Remark":"",
            "from":"Alexnet16",
            "to":"Alexnet17",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet16-Alexnet17"
        },
        {
            "Remark":"",
            "from":"Alexnet17",
            "to":"Alexnet18",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet17-Alexnet18"
        },
        {
            "Remark":"",
            "from":"Alexnet18",
            "to":"Alexnet19",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet18-Alexnet19"
        },
        {
            "Remark":"",
            "from":"Alexnet19",
            "to":"Alexnet20",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet19-Alexnet20"
        },
        {
            "Remark":"",
            "from":"Alexnet20",
            "to":"Alexnet21",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet20-Alexnet21"
        },
        {
            "Remark":"",
            "from":"Alexnet21",
            "to":"Alexnet22",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"Alexnet21-Alexnet22"
        },
        
    ],
    "nodeList":[
        {
            "attrs": {},
            "type": "input",
            "id": "Alexnet1",
            "nodeName": "input",
            "typeName": "input",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "padding": 2,
                "bias": true,
                "stride": 4,
                "in_channels": 3,
                "out_channels": 64,
                "kernel_size": 11
            },
            "type": "conv2d",
            "id": "Alexnet2",
            "nodeName": "conv2d",
            "typeName": "conv2d",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "inplace": true
            },
            "type": "relu",
            "id": "Alexnet3",
            "nodeName": "relu",
            "typeName": "relu",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "padding": 0,
                "stride": 2,
                "kernel_size": 3
            },
            "type": "maxpool2d",
            "id": "Alexnet4",
            "nodeName": "maxpool2d",
            "typeName": "maxpool2d",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "padding": 2,
                "bias": true,
                "stride": 1,
                "in_channels": 64,
                "out_channels": 192,
                "kernel_size": 5
            },
            "type": "conv2d",
            "id": "Alexnet5",
            "nodeName": "conv2d",
            "typeName": "conv2d",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "inplace": true
            },
            "type": "relu",
            "id": "Alexnet6",
            "nodeName": "relu",
            "typeName": "relu",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "padding": 0,
                "stride": 2,
                "kernel_size": 3
            },
            "type": "maxpool2d",
            "id": "Alexnet7",
            "nodeName": "maxpool2d",
            "typeName": "maxpool2d",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "padding": 1,
                "bias": true,
                "stride": 1,
                "in_channels": 192,
                "out_channels": 384,
                "kernel_size": 3
            },
            "type": "conv2d",
            "id": "Alexnet8",
            "nodeName": "conv2d",
            "typeName": "conv2d",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "inplace": true
            },
            "type": "relu",
            "id": "Alexnet9",
            "nodeName": "relu",
            "typeName": "relu",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "padding": 1,
                "bias": true,
                "stride": 1,
                "in_channels": 384,
                "out_channels": 256,
                "kernel_size": 3
            },
            "type": "conv2d",
            "id": "Alexnet10",
            "nodeName": "conv2d",
            "typeName": "conv2d",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "inplace": true
            },
            "type": "relu",
            "id": "Alexnet11",
            "nodeName": "relu",
            "typeName": "relu",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "padding": 1,
                "bias": true,
                "stride": 1,
                "in_channels": 256,
                "out_channels": 256,
                "kernel_size": 3
            },
            "type": "conv2d",
            "id": "Alexnet12",
            "nodeName": "conv2d",
            "typeName": "conv2d",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "inplace": true
            },
            "type": "relu",
            "id": "Alexnet13",
            "nodeName": "relu",
            "typeName": "relu",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "padding": 0,
                "stride": 2,
                "kernel_size": 3
            },
            "type": "maxpool2d",
            "id": "Alexnet14",
            "nodeName": "maxpool2d",
            "typeName": "maxpool2d",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {

            },
            "type": "avgpool2d",
            "id": "Alexnet15",
            "nodeName": "avgpool2d",
            "typeName": "avgpool2d",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
            },
            "type": "op_view",
            "id": "Alexnet16",
            "nodeName": "op_view",
            "typeName": "op_view",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "in_features": 9216,
                "out_features": 2048,
                "bias": true
            },
            "type": "linear",
            "id": "Alexnet17",
            "nodeName": "linear",
            "typeName": "linear",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "inplace": true
            },
            "type": "relu",
            "id": "Alexnet18",
            "nodeName": "relu",
            "typeName": "relu",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "in_features": 2048,
                "out_features": 256,
                "bias": true
            },
            "type": "linear",
            "id": "Alexnet19",
            "nodeName": "linear",
            "typeName": "linear",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "inplace": true
            },
            "type": "relu",
            "id": "Alexnet20",
            "nodeName": "relu",
            "typeName": "relu",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "in_features": 256,
                "out_features": 2,
                "bias": true
            },
            "type": "linear",
            "id": "Alexnet21",
            "nodeName": "linear",
            "typeName": "linear",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {},
            "type": "output",
            "id": "Alexnet22",
            "nodeName": "output",
            "typeName": "output",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        }
    



    ]
}
const Alexnet = {
    'type':'module_Alexnet',
    'typeName':'Alexnet',
    'nodeName':'Alexnet',
    'attrs':{},
    'log_bg_color':'rgba(250, 205, 81, 0.2)',
    ...Alexnetgraph
}

export default {Alexnet};