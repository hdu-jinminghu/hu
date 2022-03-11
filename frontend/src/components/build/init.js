const nodeTypeList = [
  {
    type: 'input',
    typeName: 'input',
    nodeName: 'input',
    log_bg_color: 'rgba(0, 128, 0, 0.2)',
    attrs:{
    }
  },{
    type: 'output',
    typeName: 'output',
    nodeName: 'output',
    log_bg_color: 'rgba(0, 128, 0, 0.2)',
    attrs:{
    }
  },
  {
    type: 'sequence',
    typeName: 'sequence',
    nodeName: 'sequence',
    log_bg_color: 'rgba(0, 128, 0, 0.2)',
    attrs:{
    }
  },
  {
  type: 'conv2d',
  typeName: 'conv2d',
  nodeName: 'conv2d',
  log_bg_color: 'rgba(0, 128, 0, 0.2)',
  attrs:{
    "in_channels":0,
    "out_channels":0,
    "kernel_size":0,
    "stride":0,
    "padding":0,
    "bias":"false"
  }
},{
  type: 'conv1d',
  typeName: 'conv1d',
  nodeName: 'conv1d',
  log_bg_color: 'rgba(255, 0, 0, 0.2)',
  attrs:{
    "in_channels":0,
    "out_channels":0,
    "kernel_size":0,
    "stride":0,
    "padding":0,
    "bias":"false"
  }
},{
  type: 'bn2d',
  typeName: 'bn2d',
  nodeName: 'bn2d',
  log_bg_color: 'rgba(0, 128, 0, 0.2)',
  attrs:{
    "num_features":0,
  }
},{
  type: 'bn1d',
  typeName: 'bn1d',
  nodeName: 'bn1d',
  log_bg_color: 'rgba(0, 128, 0, 0.2)',
  attrs:{
    "num_features":0,
  }
},{
  type: 'linear',
  typeName: 'linear',
  nodeName: 'linear',
  log_bg_color: 'rgba(132, 166, 251, 0.2)',
  attrs:{
    "in_features":0,
    "out_features":0,
    "bias":"false",
  },
},{
  type: 'relu',
  typeName: 'relu',
  nodeName: 'relu',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
  },
},{
  type: 'sigmoid',
  typeName: 'sigmoid',
  nodeName: 'sigmoid',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
  },
},{
  type: 'tanh',
  typeName: 'tanh',
  nodeName: 'tanh',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
  },
},{
  type: 'maxpool2d',
  typeName: 'maxpool2d',
  nodeName: 'maxpool2d',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
    "kernel_size":0,
    "stride":0,
    "padding":0,
    "return_indices":"false",
    "ceil_mode":"false"
  },
},{
  type: 'maxpool1d',
  typeName: 'maxpool1d',
  nodeName: 'maxpool1d',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
    "kernel_size":0,
    "stride":0,
    "padding":0,
    "return_indices":"false",
    "ceil_mode":"false"
  },
},{
  type: 'avgpool2d',
  typeName: 'avgpool2d',
  nodeName: 'avgpool2d',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
    "kernel_size":0,
    "stride":0,
    "padding":0,
    "ceil_mode":"false"
  },
},
{
  type: 'adaptiveavgpool2d',
  typeName: 'adaptiveavgpool2d',
  nodeName: 'adaptiveavgpool2d',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
  },
},{
  type: 'op_view',
  typeName: 'op_view',
  nodeName: 'op_view',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
  },
},{
  type: 'op_add',
  typeName: 'op_add',
  nodeName: 'op_add',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
  },
},{
  type: 'op_cat',
  typeName: 'op_cat',
  nodeName: 'op_cat',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
  },
},{
  type: 'op_sampling',
  typeName: 'op_sampling',
  nodeName: 'op_sampling',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
    "diff":0,
  },
}]

const opNodeList = [
  {
    type: 'op_view',
    typeName: 'op_view',
    nodeName: 'op_view',
    log_bg_color: 'rgba(250, 205, 81, 0.2)',
    attrs:{
    },
  },{
    type: 'op_add',
    typeName: 'op_add',
    nodeName: 'op_add',
    log_bg_color: 'rgba(250, 205, 81, 0.2)',
    attrs:{
    },
  },{
    type: 'op_cat',
    typeName: 'op_cat',
    nodeName: 'op_cat',
    log_bg_color: 'rgba(250, 205, 81, 0.2)',
    attrs:{
    },
  },{
    type: 'op_sampling',
    typeName: 'op_sampling',
    nodeName: 'op_sampling',
    log_bg_color: 'rgba(250, 205, 81, 0.2)',
    attrs:{
      "diff":0,
    },
  }
]

const layerNodeList = [
  {
    type: 'input',
    typeName: 'input',
    nodeName: 'input',
    log_bg_color: 'rgba(0, 128, 0, 0.2)',
    attrs:{
    }
  },{
    type: 'output',
    typeName: 'output',
    nodeName: 'output',
    log_bg_color: 'rgba(0, 128, 0, 0.2)',
    attrs:{
    }
  },
  {
    type: 'sequence',
    typeName: 'sequence',
    nodeName: 'sequence',
    log_bg_color: 'rgba(0, 128, 0, 0.2)',
    attrs:{
    }
  },
  {
  type: 'conv2d',
  typeName: 'conv2d',
  nodeName: 'conv2d',
  log_bg_color: 'rgba(0, 128, 0, 0.2)',
  attrs:{
    "in_channels":0,
    "out_channels":0,
    "kernel_size":0,
    "stride":0,
    "padding":0,
    "bias":"false"
  }
},{
  type: 'conv1d',
  typeName: 'conv1d',
  nodeName: 'conv1d',
  log_bg_color: 'rgba(255, 0, 0, 0.2)',
  attrs:{
    "in_channels":0,
    "out_channels":0,
    "kernel_size":0,
    "stride":0,
    "padding":0,
    "bias":"false"
  }
},{
  type: 'bn2d',
  typeName: 'bn2d',
  nodeName: 'bn2d',
  log_bg_color: 'rgba(0, 128, 0, 0.2)',
  attrs:{
    "num_features":0,
  }
},{
  type: 'bn1d',
  typeName: 'bn1d',
  nodeName: 'bn1d',
  log_bg_color: 'rgba(0, 128, 0, 0.2)',
  attrs:{
    "num_features":0,
  }
},{
  type: 'linear',
  typeName: 'linear',
  nodeName: 'linear',
  log_bg_color: 'rgba(132, 166, 251, 0.2)',
  attrs:{
    "in_features":0,
    "out_features":0,
    "bias":"false",
  },
},{
  type: 'relu',
  typeName: 'relu',
  nodeName: 'relu',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
  },
},{
  type: 'sigmoid',
  typeName: 'sigmoid',
  nodeName: 'sigmoid',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
  },
},{
  type: 'tanh',
  typeName: 'tanh',
  nodeName: 'tanh',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
  },
},{
  type: 'maxpool2d',
  typeName: 'maxpool2d',
  nodeName: 'maxpool2d',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
    "kernel_size":0,
    "stride":0,
    "padding":0,
    "return_indices":"false",
    "ceil_mode":"false"
  },
},{
  type: 'maxpool1d',
  typeName: 'maxpool1d',
  nodeName: 'maxpool1d',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
    "kernel_size":0,
    "stride":0,
    "padding":0,
    "return_indices":"false",
    "ceil_mode":"false"
  },
},{
  type: 'avgpool2d',
  typeName: 'avgpool2d',
  nodeName: 'avgpool2d',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
    "kernel_size":0,
    "stride":0,
    "padding":0,
    "ceil_mode":"false"
  },
},
{
  type: 'adaptiveavgpool2d',
  typeName: 'adaptiveavgpool2d',
  nodeName: 'adaptiveavgpool2d',
  log_bg_color: 'rgba(250, 205, 81, 0.2)',
  attrs:{
  },
}
]

const lossFcs = ["L1Loss","CrossEntropyLoss","SmoothL1Loss","MSELoss","BCELoss","BCEWithLogitsLoss","NLLLoss",
              "NLLLoss2d","KLDivLoss","MarginRankingLoss","MultiMarginLoss","MultiLabelMarginLoss","SoftMarginLoss",
              "MultiLabelSoftMarginLoss","CosineEmbeddingLoss"]

const datasets = ["CIFAR10","MNIST"]

const formConfig = {
  undefined:{},
  "input":{
  },
  "output":{
  },
  "sequence":{
  },
  "conv2d":{
      "in_channels":0,
      "out_channels":0,
      "kernel_size":0,
      "stride":0,
      "padding":0,
      "bias":"false",
  },
  "conv1d":{
      "in_channels":0,
      "out_channels":0,
      "kernel_size":0,
      "stride":0,
      "padding":0,
      "bias":"false",
  },
  "bn2d":{
      "num_features":0,
  },
  "bn1d":{
      "num_features":0,
  },
  "linear":{
      "in_features":0,
      "out_features":0,
      "bias":"false",
  },
  "relu":{
  },
  "sigmoid":{
  },
  "tanh":{
  },
  "maxpool2d":{
      "kernel_size":0,
      "stride":0,
      "padding":0,
      "return_indices":"false",
      "ceil_mode":"false"
  },
  "maxpool1d":{
      "kernel_size":0,
      "stride":0,
      "padding":0,
      "return_indices":"false",
      "ceil_mode":"false"
  },
  "adaptiveavgpool2d":{
  },
  "op_view":{
  },
  "op_add":{
  },
  "op_cat":{
  },
  "op_sampling":{
    "diff":0
  }
}

const optims = ['Adam','SGD','Rprop','Adamax','Adagrad','Adadelta']

export {nodeTypeList,lossFcs,datasets,formConfig,opNodeList,layerNodeList,optims};