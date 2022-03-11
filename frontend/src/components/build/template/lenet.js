const LeNetGraph = {
    "lineList":[
        {
            "Remark":"",
            "from":"letnet1",
            "to":"letnet2",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"letnet1-letnet2"
        },
        {
            "Remark":"",
            "from":"letnet2",
            "to":"letnet3",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"letnet2-letnet3"
        },
        {
            "Remark":"",
            "from":"letnet3",
            "to":"letnet4",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"letnet3-letnet4"
        },
        {
            "Remark":"",
            "from":"letnet4",
            "to":"letnet5",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"letnet4-letnet5"
        },
        {
            "Remark":"",
            "from":"letnet5",
            "to":"letnet6",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"letnet5-letnet6"
        },
        {
            "Remark":"",
            "from":"letnet6",
            "to":"letnet7",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"letnet6-letnet7"
        },
        {
            "Remark":"",
            "from":"letnet7",
            "to":"letnet8",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"letnet7-letnet8"
        },
        {
            "Remark":"",
            "from":"letnet8",
            "to":"letnet9",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"letnet8-letnet9"
        },
        {
            "Remark":"",
            "from":"letnet9",
            "to":"letnet10",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"letnet9-letnet10"
        },
        {
            "Remark":"",
            "from":"letnet10",
            "to":"letnet11",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"letnet10-letnet11"
        },
        {
            "Remark":"",
            "from":"letnet11",
            "to":"letnet12",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"letnet11-letnet12"
        },
        {
            "Remark":"",
            "from":"letnet12",
            "to":"letnet13",
            "label":"\u8fde\u7ebf\u540d\u79f0",
            "id":"letnet12-letnet13"
        },
    ],
    "nodeList":[
        {
            "attrs": {},
            "type": "input",
            "id": "letnet1",
            "nodeName": "input",
            "typeName": "input",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "padding": 0,
                "bias": true,
                "stride": 1,
                "in_channels": 3,
                "out_channels": 6,
                "kernel_size": 5
            },
            "type": "conv2d",
            "id": "letnet2",
            "nodeName": "conv2d",
            "typeName": "conv2d",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "inplace": true
            },
            "type": "relu",
            "id": "letnet3",
            "nodeName": "relu",
            "typeName": "relu",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "padding": 0,
                "bias": true,
                "stride": 1,
                "in_channels": 6,
                "out_channels": 16,
                "kernel_size": 5
            },
            "type": "conv2d",
            "id": "letnet4",
            "nodeName": "conv2d",
            "typeName": "conv2d",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "inplace": true
            },
            "type": "relu",
            "id": "letnet5",
            "nodeName": "relu",
            "typeName": "relu",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "padding": 0,
                "bias": true,
                "stride": 1,
                "in_channels": 16,
                "out_channels": 16,
                "kernel_size": 5
            },
            "type": "conv2d",
            "id": "letnet6",
            "nodeName": "conv2d",
            "typeName": "conv2d",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "inplace": true
            },
            "type": "relu",
            "id": "letnet7",
            "nodeName": "relu",
            "typeName": "relu",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "padding": 0,
                "bias": true,
                "stride": 1,
                "in_channels": 16,
                "out_channels": 16,
                "kernel_size": 5
            },
            "type": "conv2d",
            "id": "letnet8",
            "nodeName": "conv2d",
            "typeName": "conv2d",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
            },
            "type": "op_view",
            "id": "letnet9",
            "nodeName": "op_view",
            "typeName": "op_view",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "in_features": 400,
                "out_features": 120,
                "bias": true
            },
            "type": "linear",
            "id": "letnet10",
            "nodeName": "linear",
            "typeName": "linear",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "in_features": 120,
                "out_features": 84,
                "bias": true
            },
            "type": "linear",
            "id": "letnet11",
            "nodeName": "linear",
            "typeName": "linear",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {
                "in_features": 84,
                "out_features": 10,
                "bias": true
            },
            "type": "linear",
            "id": "letnet12",
            "nodeName": "linear",
            "typeName": "linear",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        },
        {
            "attrs": {},
            "type": "output",
            "id": "letnet13",
            "nodeName": "output",
            "typeName": "output",
            "log_bg_color": "rgba(250, 205, 81, 0.2)"
        }
    
    ]

}

const Lenet = {
    'type':'module_LeNet',
    'typeName':'Lenet',
    'nodeName':'Lenet',
    'attrs':{},
    'log_bg_color':'rgba(250, 205, 81, 0.2)',
    ...LeNetGraph
}

export default{Lenet}