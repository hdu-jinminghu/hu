const resBottleNeck1 = {
	"lineList": [{
		"Remark": "",
		"from": "bottleneck1_0",
		"to": "bottleneck1_1",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_0-bottleneck1_1"
	}, {
		"Remark": "",
		"from": "bottleneck1_0",
		"to": "bottleneck1_9",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_0-bottleneck1_9"
	}, {
		"Remark": "",
		"from": "bottleneck1_1",
		"to": "bottleneck1_2",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_1-bottleneck1_2"
	}, {
		"Remark": "",
		"from": "bottleneck1_2",
		"to": "bottleneck1_3",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_2-bottleneck1_3"
	}, {
		"Remark": "",
		"from": "bottleneck1_3",
		"to": "bottleneck1_4",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_3-bottleneck1_4"
	}, {
		"Remark": "",
		"from": "bottleneck1_4",
		"to": "bottleneck1_5",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_4-bottleneck1_5"
	}, {
		"Remark": "",
		"from": "bottleneck1_5",
		"to": "bottleneck1_6",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_5-bottleneck1_6"
	}, {
		"Remark": "",
		"from": "bottleneck1_6",
		"to": "bottleneck1_7",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_6-bottleneck1_7"
	}, {
		"Remark": "",
		"from": "bottleneck1_7",
		"to": "bottleneck1_8",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_7-bottleneck1_8"
	}, {
		"Remark": "",
		"from": "bottleneck1_8",
		"to": "bottleneck1_11",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_8-bottleneck1_11"
	}, {
		"Remark": "",
		"from": "bottleneck1_9",
		"to": "bottleneck1_10",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_9-bottleneck1_10"
	}, {
		"Remark": "",
		"from": "bottleneck1_10",
		"to": "bottleneck1_11",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_10-bottleneck1_11"
	}, {
		"Remark": "",
		"from": "bottleneck1_11",
		"to": "bottleneck1_12",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_11-bottleneck1_12"
	}, {
		"Remark": "",
		"from": "bottleneck1_12",
		"to": "bottleneck1_13",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck1_12-bottleneck1_13"
	}],
	"nodeList": [{
		"attrs": {},
		"type": "input",
		"id": "bottleneck1_0",
		"nodeName": "input",
		"typeName": "input",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 64,
			"out_channels": 64,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck1_1",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 64
		},
		"type": "bn2d",
		"id": "bottleneck1_2",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck1_3",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 1,
			"bias": true,
			"stride": 1,
			"in_channels": 64,
			"out_channels": 64,
			"kernel_size": 3
		},
		"type": "conv2d",
		"id": "bottleneck1_4",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 64
		},
		"type": "bn2d",
		"id": "bottleneck1_5",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck1_6",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 64,
			"out_channels": 256,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck1_7",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 256
		},
		"type": "bn2d",
		"id": "bottleneck1_8",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 64,
			"out_channels": 256,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck1_9",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 256
		},
		"type": "bn2d",
		"id": "bottleneck1_10",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "op_add",
		"id": "bottleneck1_11",
		"nodeName": "op_add",
		"typeName": "op_add",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck1_12",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "output",
		"id": "bottleneck1_13",
		"nodeName": "output",
		"typeName": "output",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}],
	"attrs":{
		"in_channels":64,
		"out_channels":256
	}
}

const resBottleNeck2 = {
	"lineList": [{
		"Remark": "",
		"from": "bottleneck2_0",
		"to": "bottleneck2_1",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck2_0-bottleneck2_1"
	}, {
		"Remark": "",
		"from": "bottleneck2_0",
		"to": "bottleneck2_9",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck2_0-bottleneck2_9"
	}, {
		"Remark": "",
		"from": "bottleneck2_1",
		"to": "bottleneck2_2",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck2_1-bottleneck2_2"
	}, {
		"Remark": "",
		"from": "bottleneck2_2",
		"to": "bottleneck2_3",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck2_2-bottleneck2_3"
	}, {
		"Remark": "",
		"from": "bottleneck2_3",
		"to": "bottleneck2_4",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck2_3-bottleneck2_4"
	}, {
		"Remark": "",
		"from": "bottleneck2_4",
		"to": "bottleneck2_5",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck2_4-bottleneck2_5"
	}, {
		"Remark": "",
		"from": "bottleneck2_5",
		"to": "bottleneck2_6",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck2_5-bottleneck2_6"
	}, {
		"Remark": "",
		"from": "bottleneck2_6",
		"to": "bottleneck2_7",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck2_6-bottleneck2_7"
	}, {
		"Remark": "",
		"from": "bottleneck2_7",
		"to": "bottleneck2_8",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck2_7-bottleneck2_8"
	}, {
		"Remark": "",
		"from": "bottleneck2_8",
		"to": "bottleneck2_9",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck2_8-bottleneck2_9"
	}, {
		"Remark": "",
		"from": "bottleneck2_9",
		"to": "bottleneck2_10",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck2_9-bottleneck2_10"
	}, {
		"Remark": "",
		"from": "bottleneck2_10",
		"to": "bottleneck2_11",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck2_10-bottleneck2_11"
	}],
	"nodeList": [{
		"attrs": {},
		"type": "input",
		"id": "bottleneck2_0",
		"nodeName": "input",
		"typeName": "input",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 256,
			"out_channels": 64,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck2_1",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 64
		},
		"type": "bn2d",
		"id": "bottleneck2_2",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck2_3",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 1,
			"bias": true,
			"stride": 1,
			"in_channels": 64,
			"out_channels": 64,
			"kernel_size": 3
		},
		"type": "conv2d",
		"id": "bottleneck2_4",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 64
		},
		"type": "bn2d",
		"id": "bottleneck2_5",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck2_6",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 64,
			"out_channels": 256,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck2_7",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 256
		},
		"type": "bn2d",
		"id": "bottleneck2_8",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "op_add",
		"id": "bottleneck2_9",
		"nodeName": "op_add",
		"typeName": "op_add",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck2_10",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "output",
		"id": "bottleneck2_11",
		"nodeName": "output",
		"typeName": "output",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}],
	"attrs":{
		"in_channels":256,
		"out_channels":256
	}
}
const resBottleNeck3 = {
	"lineList": [{
		"Remark": "",
		"from": "bottleneck3_0",
		"to": "bottleneck3_1",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_0-bottleneck3_1"
	}, {
		"Remark": "",
		"from": "bottleneck3_0",
		"to": "bottleneck3_9",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_0-bottleneck3_9"
	}, {
		"Remark": "",
		"from": "bottleneck3_1",
		"to": "bottleneck3_2",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_1-bottleneck3_2"
	}, {
		"Remark": "",
		"from": "bottleneck3_2",
		"to": "bottleneck3_3",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_2-bottleneck3_3"
	}, {
		"Remark": "",
		"from": "bottleneck3_3",
		"to": "bottleneck3_4",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_3-bottleneck3_4"
	}, {
		"Remark": "",
		"from": "bottleneck3_4",
		"to": "bottleneck3_5",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_4-bottleneck3_5"
	}, {
		"Remark": "",
		"from": "bottleneck3_5",
		"to": "bottleneck3_6",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_5-bottleneck3_6"
	}, {
		"Remark": "",
		"from": "bottleneck3_6",
		"to": "bottleneck3_7",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_6-bottleneck3_7"
	}, {
		"Remark": "",
		"from": "bottleneck3_7",
		"to": "bottleneck3_8",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_7-bottleneck3_8"
	}, {
		"Remark": "",
		"from": "bottleneck3_8",
		"to": "bottleneck3_11",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_8-bottleneck3_11"
	}, {
		"Remark": "",
		"from": "bottleneck3_9",
		"to": "bottleneck3_10",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_9-bottleneck3_10"
	}, {
		"Remark": "",
		"from": "bottleneck3_10",
		"to": "bottleneck3_11",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_10-bottleneck3_11"
	}, {
		"Remark": "",
		"from": "bottleneck3_11",
		"to": "bottleneck3_12",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_11-bottleneck3_12"
	}, {
		"Remark": "",
		"from": "bottleneck3_12",
		"to": "bottleneck3_13",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck3_12-bottleneck3_13"
	}],
	"nodeList": [{
		"attrs": {},
		"type": "input",
		"id": "bottleneck3_0",
		"nodeName": "input",
		"typeName": "input",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 256,
			"out_channels": 128,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck3_1",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 128
		},
		"type": "bn2d",
		"id": "bottleneck3_2",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck3_3",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 1,
			"bias": true,
			"stride": 2,
			"in_channels": 128,
			"out_channels": 128,
			"kernel_size": 3
		},
		"type": "conv2d",
		"id": "bottleneck3_4",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 128
		},
		"type": "bn2d",
		"id": "bottleneck3_5",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck3_6",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 128,
			"out_channels": 512,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck3_7",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 512
		},
		"type": "bn2d",
		"id": "bottleneck3_8",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 2,
			"in_channels": 256,
			"out_channels": 512,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck3_9",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 512
		},
		"type": "bn2d",
		"id": "bottleneck3_10",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "op_add",
		"id": "bottleneck3_11",
		"nodeName": "op_add",
		"typeName": "op_add",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck3_12",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "output",
		"id": "bottleneck3_13",
		"nodeName": "output",
		"typeName": "output",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}],
	"attrs":{
		"in_channels":256,
		"out_channels":512
	}
}

const resBottleNeck4 = {
	"lineList": [{
		"Remark": "",
		"from": "bottleneck4_0",
		"to": "bottleneck4_1",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck4_0-bottleneck4_1"
	}, {
		"Remark": "",
		"from": "bottleneck4_0",
		"to": "bottleneck4_9",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck4_0-bottleneck4_9"
	}, {
		"Remark": "",
		"from": "bottleneck4_1",
		"to": "bottleneck4_2",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck4_1-bottleneck4_2"
	}, {
		"Remark": "",
		"from": "bottleneck4_2",
		"to": "bottleneck4_3",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck4_2-bottleneck4_3"
	}, {
		"Remark": "",
		"from": "bottleneck4_3",
		"to": "bottleneck4_4",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck4_3-bottleneck4_4"
	}, {
		"Remark": "",
		"from": "bottleneck4_4",
		"to": "bottleneck4_5",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck4_4-bottleneck4_5"
	}, {
		"Remark": "",
		"from": "bottleneck4_5",
		"to": "bottleneck4_6",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck4_5-bottleneck4_6"
	}, {
		"Remark": "",
		"from": "bottleneck4_6",
		"to": "bottleneck4_7",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck4_6-bottleneck4_7"
	}, {
		"Remark": "",
		"from": "bottleneck4_7",
		"to": "bottleneck4_8",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck4_7-bottleneck4_8"
	}, {
		"Remark": "",
		"from": "bottleneck4_8",
		"to": "bottleneck4_9",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck4_8-bottleneck4_9"
	}, {
		"Remark": "",
		"from": "bottleneck4_9",
		"to": "bottleneck4_10",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck4_9-bottleneck4_10"
	}, {
		"Remark": "",
		"from": "bottleneck4_10",
		"to": "bottleneck4_11",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck4_10-bottleneck4_11"
	}],
	"nodeList": [{
		"attrs": {},
		"type": "input",
		"id": "bottleneck4_0",
		"nodeName": "input",
		"typeName": "input",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 512,
			"out_channels": 128,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck4_1",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 128
		},
		"type": "bn2d",
		"id": "bottleneck4_2",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck4_3",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 1,
			"bias": true,
			"stride": 1,
			"in_channels": 128,
			"out_channels": 128,
			"kernel_size": 3
		},
		"type": "conv2d",
		"id": "bottleneck4_4",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 128
		},
		"type": "bn2d",
		"id": "bottleneck4_5",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck4_6",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 128,
			"out_channels": 512,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck4_7",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 512
		},
		"type": "bn2d",
		"id": "bottleneck4_8",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "op_add",
		"id": "bottleneck4_9",
		"nodeName": "op_add",
		"typeName": "op_add",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck4_10",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "output",
		"id": "bottleneck4_11",
		"nodeName": "output",
		"typeName": "output",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}],
	"attrs":{
		"in_channels":512,
		"out_channels":512
	}
}

const resBottleNeck5 = {
	"lineList": [{
		"Remark": "",
		"from": "bottleneck5_0",
		"to": "bottleneck5_1",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_0-bottleneck5_1"
	}, {
		"Remark": "",
		"from": "bottleneck5_0",
		"to": "bottleneck5_9",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_0-bottleneck5_9"
	}, {
		"Remark": "",
		"from": "bottleneck5_1",
		"to": "bottleneck5_2",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_1-bottleneck5_2"
	}, {
		"Remark": "",
		"from": "bottleneck5_2",
		"to": "bottleneck5_3",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_2-bottleneck5_3"
	}, {
		"Remark": "",
		"from": "bottleneck5_3",
		"to": "bottleneck5_4",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_3-bottleneck5_4"
	}, {
		"Remark": "",
		"from": "bottleneck5_4",
		"to": "bottleneck5_5",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_4-bottleneck5_5"
	}, {
		"Remark": "",
		"from": "bottleneck5_5",
		"to": "bottleneck5_6",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_5-bottleneck5_6"
	}, {
		"Remark": "",
		"from": "bottleneck5_6",
		"to": "bottleneck5_7",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_6-bottleneck5_7"
	}, {
		"Remark": "",
		"from": "bottleneck5_7",
		"to": "bottleneck5_8",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_7-bottleneck5_8"
	}, {
		"Remark": "",
		"from": "bottleneck5_8",
		"to": "bottleneck5_11",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_8-bottleneck5_11"
	}, {
		"Remark": "",
		"from": "bottleneck5_9",
		"to": "bottleneck5_10",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_9-bottleneck5_10"
	}, {
		"Remark": "",
		"from": "bottleneck5_10",
		"to": "bottleneck5_11",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_10-bottleneck5_11"
	}, {
		"Remark": "",
		"from": "bottleneck5_11",
		"to": "bottleneck5_12",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_11-bottleneck5_12"
	}, {
		"Remark": "",
		"from": "bottleneck5_12",
		"to": "bottleneck5_13",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck5_12-bottleneck5_13"
	}],
	"nodeList": [{
		"attrs": {},
		"type": "input",
		"id": "bottleneck5_0",
		"nodeName": "input",
		"typeName": "input",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 512,
			"out_channels": 256,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck5_1",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 256
		},
		"type": "bn2d",
		"id": "bottleneck5_2",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck5_3",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 1,
			"bias": true,
			"stride": 2,
			"in_channels": 256,
			"out_channels": 256,
			"kernel_size": 3
		},
		"type": "conv2d",
		"id": "bottleneck5_4",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 256
		},
		"type": "bn2d",
		"id": "bottleneck5_5",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck5_6",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 256,
			"out_channels": 1024,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck5_7",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 1024
		},
		"type": "bn2d",
		"id": "bottleneck5_8",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 2,
			"in_channels": 512,
			"out_channels": 1024,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck5_9",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 1024
		},
		"type": "bn2d",
		"id": "bottleneck5_10",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "op_add",
		"id": "bottleneck5_11",
		"nodeName": "op_add",
		"typeName": "op_add",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck5_12",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "output",
		"id": "bottleneck5_13",
		"nodeName": "output",
		"typeName": "output",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}],
	"attrs":{
		"in_channels":512,
		"out_channels":1024
	}
}

const resBottleNeck6 = {
	"lineList": [{
		"Remark": "",
		"from": "bottleneck6_0",
		"to": "bottleneck6_1",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck6_0-bottleneck6_1"
	}, {
		"Remark": "",
		"from": "bottleneck6_0",
		"to": "bottleneck6_9",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck6_0-bottleneck6_9"
	}, {
		"Remark": "",
		"from": "bottleneck6_1",
		"to": "bottleneck6_2",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck6_1-bottleneck6_2"
	}, {
		"Remark": "",
		"from": "bottleneck6_2",
		"to": "bottleneck6_3",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck6_2-bottleneck6_3"
	}, {
		"Remark": "",
		"from": "bottleneck6_3",
		"to": "bottleneck6_4",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck6_3-bottleneck6_4"
	}, {
		"Remark": "",
		"from": "bottleneck6_4",
		"to": "bottleneck6_5",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck6_4-bottleneck6_5"
	}, {
		"Remark": "",
		"from": "bottleneck6_5",
		"to": "bottleneck6_6",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck6_5-bottleneck6_6"
	}, {
		"Remark": "",
		"from": "bottleneck6_6",
		"to": "bottleneck6_7",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck6_6-bottleneck6_7"
	}, {
		"Remark": "",
		"from": "bottleneck6_7",
		"to": "bottleneck6_8",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck6_7-bottleneck6_8"
	}, {
		"Remark": "",
		"from": "bottleneck6_8",
		"to": "bottleneck6_9",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck6_8-bottleneck6_9"
	}, {
		"Remark": "",
		"from": "bottleneck6_9",
		"to": "bottleneck6_10",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck6_9-bottleneck6_10"
	}, {
		"Remark": "",
		"from": "bottleneck6_10",
		"to": "bottleneck6_11",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck6_10-bottleneck6_11"
	}],
	"nodeList": [{
		"attrs": {},
		"type": "input",
		"id": "bottleneck6_0",
		"nodeName": "input",
		"typeName": "input",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 1024,
			"out_channels": 256,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck6_1",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 256
		},
		"type": "bn2d",
		"id": "bottleneck6_2",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck6_3",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 1,
			"bias": true,
			"stride": 1,
			"in_channels": 256,
			"out_channels": 256,
			"kernel_size": 3
		},
		"type": "conv2d",
		"id": "bottleneck6_4",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 256
		},
		"type": "bn2d",
		"id": "bottleneck6_5",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck6_6",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 256,
			"out_channels": 1024,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck6_7",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 1024
		},
		"type": "bn2d",
		"id": "bottleneck6_8",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "op_add",
		"id": "bottleneck6_9",
		"nodeName": "op_add",
		"typeName": "op_add",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck6_10",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "output",
		"id": "bottleneck6_11",
		"nodeName": "output",
		"typeName": "output",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}],
	"attrs":{
		"in_channels":1024,
		"out_channels":1024
	}
}

const resBottleNeck7 = {
	"lineList": [{
		"Remark": "",
		"from": "bottleneck7_0",
		"to": "bottleneck7_1",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_0-bottleneck7_1"
	}, {
		"Remark": "",
		"from": "bottleneck7_0",
		"to": "bottleneck7_9",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_0-bottleneck7_9"
	}, {
		"Remark": "",
		"from": "bottleneck7_1",
		"to": "bottleneck7_2",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_1-bottleneck7_2"
	}, {
		"Remark": "",
		"from": "bottleneck7_2",
		"to": "bottleneck7_3",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_2-bottleneck7_3"
	}, {
		"Remark": "",
		"from": "bottleneck7_3",
		"to": "bottleneck7_4",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_3-bottleneck7_4"
	}, {
		"Remark": "",
		"from": "bottleneck7_4",
		"to": "bottleneck7_5",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_4-bottleneck7_5"
	}, {
		"Remark": "",
		"from": "bottleneck7_5",
		"to": "bottleneck7_6",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_5-bottleneck7_6"
	}, {
		"Remark": "",
		"from": "bottleneck7_6",
		"to": "bottleneck7_7",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_6-bottleneck7_7"
	}, {
		"Remark": "",
		"from": "bottleneck7_7",
		"to": "bottleneck7_8",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_7-bottleneck7_8"
	}, {
		"Remark": "",
		"from": "bottleneck7_8",
		"to": "bottleneck7_11",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_8-bottleneck7_11"
	}, {
		"Remark": "",
		"from": "bottleneck7_9",
		"to": "bottleneck7_10",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_9-bottleneck7_10"
	}, {
		"Remark": "",
		"from": "bottleneck7_10",
		"to": "bottleneck7_11",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_10-bottleneck7_11"
	}, {
		"Remark": "",
		"from": "bottleneck7_11",
		"to": "bottleneck7_12",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_11-bottleneck7_12"
	}, {
		"Remark": "",
		"from": "bottleneck7_12",
		"to": "bottleneck7_13",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck7_12-bottleneck7_13"
	}],
	"nodeList": [{
		"attrs": {},
		"type": "input",
		"id": "bottleneck7_0",
		"nodeName": "input",
		"typeName": "input",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 1024,
			"out_channels": 512,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck7_1",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 512
		},
		"type": "bn2d",
		"id": "bottleneck7_2",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck7_3",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 1,
			"bias": true,
			"stride": 2,
			"in_channels": 512,
			"out_channels": 512,
			"kernel_size": 3
		},
		"type": "conv2d",
		"id": "bottleneck7_4",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 512
		},
		"type": "bn2d",
		"id": "bottleneck7_5",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck7_6",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 512,
			"out_channels": 2048,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck7_7",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 2048
		},
		"type": "bn2d",
		"id": "bottleneck7_8",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 2,
			"in_channels": 1024,
			"out_channels": 2048,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck7_9",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 2048
		},
		"type": "bn2d",
		"id": "bottleneck7_10",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "op_add",
		"id": "bottleneck7_11",
		"nodeName": "op_add",
		"typeName": "op_add",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck7_12",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "output",
		"id": "bottleneck7_13",
		"nodeName": "output",
		"typeName": "output",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}],
	"attrs":{
		"in_channels":1024,
		"out_channels":2048
	}
}

const resBottleNeck8 = {
	"lineList": [{
		"Remark": "",
		"from": "bottleneck8_0",
		"to": "bottleneck8_1",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck8_0-bottleneck8_1"
	}, {
		"Remark": "",
		"from": "bottleneck8_0",
		"to": "bottleneck8_9",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck8_0-bottleneck8_9"
	}, {
		"Remark": "",
		"from": "bottleneck8_1",
		"to": "bottleneck8_2",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck8_1-bottleneck8_2"
	}, {
		"Remark": "",
		"from": "bottleneck8_2",
		"to": "bottleneck8_3",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck8_2-bottleneck8_3"
	}, {
		"Remark": "",
		"from": "bottleneck8_3",
		"to": "bottleneck8_4",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck8_3-bottleneck8_4"
	}, {
		"Remark": "",
		"from": "bottleneck8_4",
		"to": "bottleneck8_5",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck8_4-bottleneck8_5"
	}, {
		"Remark": "",
		"from": "bottleneck8_5",
		"to": "bottleneck8_6",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck8_5-bottleneck8_6"
	}, {
		"Remark": "",
		"from": "bottleneck8_6",
		"to": "bottleneck8_7",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck8_6-bottleneck8_7"
	}, {
		"Remark": "",
		"from": "bottleneck8_7",
		"to": "bottleneck8_8",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck8_7-bottleneck8_8"
	}, {
		"Remark": "",
		"from": "bottleneck8_8",
		"to": "bottleneck8_9",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck8_8-bottleneck8_9"
	}, {
		"Remark": "",
		"from": "bottleneck8_9",
		"to": "bottleneck8_10",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck8_9-bottleneck8_10"
	}, {
		"Remark": "",
		"from": "bottleneck8_10",
		"to": "bottleneck8_11",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "bottleneck8_10-bottleneck8_11"
	}],
	"nodeList": [{
		"attrs": {},
		"type": "input",
		"id": "bottleneck8_0",
		"nodeName": "input",
		"typeName": "input",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 2048,
			"out_channels": 512,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck8_1",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 512
		},
		"type": "bn2d",
		"id": "bottleneck8_2",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck8_3",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 1,
			"bias": true,
			"stride": 1,
			"in_channels": 512,
			"out_channels": 512,
			"kernel_size": 3
		},
		"type": "conv2d",
		"id": "bottleneck8_4",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 512
		},
		"type": "bn2d",
		"id": "bottleneck8_5",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck8_6",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 0,
			"bias": true,
			"stride": 1,
			"in_channels": 512,
			"out_channels": 2048,
			"kernel_size": 1
		},
		"type": "conv2d",
		"id": "bottleneck8_7",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 2048
		},
		"type": "bn2d",
		"id": "bottleneck8_8",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "op_add",
		"id": "bottleneck8_9",
		"nodeName": "op_add",
		"typeName": "op_add",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "bottleneck8_10",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "output",
		"id": "bottleneck8_11",
		"nodeName": "output",
		"typeName": "output",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}],
	"attrs":{
		"in_channels":2048,
		"out_channels":2048
	}
}

const resnet50 = {
	"lineList": [{
		"Remark": "",
		"from": "resnetVertex1",
		"to": "resnetVertex2",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex1-resnetVertex2"
	}, {
		"Remark": "",
		"from": "resnetVertex2",
		"to": "resnetVertex3",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex2-resnetVertex3"
	}, {
		"Remark": "",
		"from": "resnetVertex3",
		"to": "resnetVertex4",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex3-resnetVertex4"
	}, {
		"Remark": "",
		"from": "resnetVertex4",
		"to": "resnetVertex5",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex4-resnetVertex5"
	}, {
		"Remark": "",
		"from": "resnetVertex5",
		"to": "resnetVertex6",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex5-resnetVertex6"
	}, {
		"Remark": "",
		"from": "resnetVertex6",
		"to": "resnetVertex7",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex6-resnetVertex7"
	}, {
		"Remark": "",
		"from": "resnetVertex7",
		"to": "resnetVertex8",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex7-resnetVertex8"
	}, {
		"Remark": "",
		"from": "resnetVertex8",
		"to": "resnetVertex9",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex8-resnetVertex9"
	}, {
		"Remark": "",
		"from": "resnetVertex9",
		"to": "resnetVertex10",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex9-resnetVertex10"
	}, {
		"Remark": "",
		"from": "resnetVertex10",
		"to": "resnetVertex11",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex10-resnetVertex11"
	}, {
		"Remark": "",
		"from": "resnetVertex11",
		"to": "resnetVertex12",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex11-resnetVertex12"
	}, {
		"Remark": "",
		"from": "resnetVertex12",
		"to": "resnetVertex13",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex12-resnetVertex13"
	}, {
		"Remark": "",
		"from": "resnetVertex13",
		"to": "resnetVertex14",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex13-resnetVertex14"
	}, {
		"Remark": "",
		"from": "resnetVertex14",
		"to": "resnetVertex15",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex14-resnetVertex15"
	}, {
		"Remark": "",
		"from": "resnetVertex15",
		"to": "resnetVertex16",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex15-resnetVertex16"
	}, {
		"Remark": "",
		"from": "resnetVertex16",
		"to": "resnetVertex17",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex16-resnetVertex17"
	}, {
		"Remark": "",
		"from": "resnetVertex17",
		"to": "resnetVertex18",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex17-resnetVertex18"
	}, {
		"Remark": "",
		"from": "resnetVertex18",
		"to": "resnetVertex19",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex18-resnetVertex19"
	}, {
		"Remark": "",
		"from": "resnetVertex19",
		"to": "resnetVertex20",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex19-resnetVertex20"
	}, {
		"Remark": "",
		"from": "resnetVertex20",
		"to": "resnetVertex21",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex20-resnetVertex21"
	}, {
		"Remark": "",
		"from": "resnetVertex21",
		"to": "resnetVertex22",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex21-resnetVertex22"
	}, {
		"Remark": "",
		"from": "resnetVertex22",
		"to": "resnetVertex23",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex22-resnetVertex23"
	}, {
		"Remark": "",
		"from": "resnetVertex23",
		"to": "resnetVertex24",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex23-resnetVertex24"
	}, {
		"Remark": "",
		"from": "resnetVertex24",
		"to": "resnetVertex25",
		"label": "\u8fde\u7ebf\u540d\u79f0",
		"id": "resnetVertex24-resnetVertex25"
	}],
	"nodeList": [{
		"attrs": {},
		"type": "input",
		"id": "resnetVertex1",
		"nodeName": "input",
		"typeName": "input",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 3,
			"bias": true,
			"stride": 2,
			"in_channels": 3,
			"out_channels": 64,
			"kernel_size": 7
		},
		"type": "conv2d",
		"id": "resnetVertex2",
		"nodeName": "conv2d",
		"typeName": "conv2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"num_features": 64
		},
		"type": "bn2d",
		"id": "resnetVertex3",
		"nodeName": "bn2d",
		"typeName": "bn2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"inplace": true
		},
		"type": "relu",
		"id": "resnetVertex4",
		"nodeName": "relu",
		"typeName": "relu",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"padding": 1,
			"stride": 2,
			"kernel_size": 3
		},
		"type": "maxpool2d",
		"id": "resnetVertex5",
		"nodeName": "maxpool2d",
		"typeName": "maxpool2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "resBottleNeck1",
		"id": "resnetVertex6",
		"nodeName": "resBottleNeck1",
		"typeName": "resBottleNeck1",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck1))
	}, {
		"attrs": {},
		"type": "resBottleNeck2",
		"id": "resnetVertex7",
		"nodeName": "resBottleNeck2",
		"typeName": "resBottleNeck2",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck2))
	}, {
		"attrs": {},
		"type": "resBottleNeck2",
		"id": "resnetVertex8",
		"nodeName": "resBottleNeck2",
		"typeName": "resBottleNeck2",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck2))
	}, {
		"attrs": {},
		"type": "resBottleNeck3",
		"id": "resnetVertex9",
		"nodeName": "resBottleNeck3",
		"typeName": "resBottleNeck3",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck3))
	}, {
		"attrs": {},
		"type": "resBottleNeck4",
		"id": "resnetVertex10",
		"nodeName": "resBottleNeck4",
		"typeName": "resBottleNeck4",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck4))
	}, {
		"attrs": {},
		"type": "resBottleNeck4",
		"id": "resnetVertex11",
		"nodeName": "resBottleNeck4",
		"typeName": "resBottleNeck4",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck4))
	}, {
		"attrs": {},
		"type": "resBottleNeck4",
		"id": "resnetVertex12",
		"nodeName": "resBottleNeck4",
		"typeName": "resBottleNeck4",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck4))
	}, {
		"attrs": {},
		"type": "resBottleNeck5",
		"id": "resnetVertex13",
		"nodeName": "resBottleNeck5",
		"typeName": "resBottleNeck5",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck5))
	}, {
		"attrs": {},
		"type": "resBottleNeck6",
		"id": "resnetVertex14",
		"nodeName": "resBottleNeck6",
		"typeName": "resBottleNeck6",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck6))
	}, {
		"attrs": {},
		"type": "resBottleNeck6",
		"id": "resnetVertex15",
		"nodeName": "resBottleNeck6",
		"typeName": "resBottleNeck6",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck6))
	}, {
		"attrs": {},
		"type": "resBottleNeck6",
		"id": "resnetVertex16",
		"nodeName": "resBottleNeck6",
		"typeName": "resBottleNeck6",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck6))
	}, {
		"attrs": {},
		"type": "resBottleNeck6",
		"id": "resnetVertex17",
		"nodeName": "resBottleNeck6",
		"typeName": "resBottleNeck6",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck6))
	}, {
		"attrs": {},
		"type": "resBottleNeck6",
		"id": "resnetVertex18",
		"nodeName": "resBottleNeck6",
		"typeName": "resBottleNeck6",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck6))
	}, {
		"attrs": {},
		"type": "resBottleNeck7",
		"id": "resnetVertex19",
		"nodeName": "resBottleNeck7",
		"typeName": "resBottleNeck7",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck7))
	}, {
		"attrs": {},
		"type": "resBottleNeck8",
		"id": "resnetVertex20",
		"nodeName": "resBottleNeck8",
		"typeName": "resBottleNeck8",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck8))
	}, {
		"attrs": {},
		"type": "resBottleNeck8",
		"id": "resnetVertex21",
		"nodeName": "resBottleNeck8",
		"typeName": "resBottleNeck8",
		"log_bg_color": "rgba(250, 205, 81, 0.2)",
		...JSON.parse(JSON.stringify(resBottleNeck8))
	}, {
		"attrs": {},
		"type": "adaptiveavgpool2d",
		"id": "resnetVertex22",
		"nodeName": "adaptiveavgpool2d",
		"typeName": "adaptiveavgpool2d",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "op_view",
		"id": "resnetVertex23",
		"nodeName": "op_view",
		"typeName": "op_view",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {
			"in_features": 2048,
			"out_features": 10,
			"bias": true
		},
		"type": "linear",
		"id": "resnetVertex24",
		"nodeName": "linear",
		"typeName": "linear",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}, {
		"attrs": {},
		"type": "output",
		"id": "resnetVertex25",
		"nodeName": "output",
		"typeName": "output",
		"log_bg_color": "rgba(250, 205, 81, 0.2)"
	}]
}

export default {resnet50,resBottleNeck1,resBottleNeck2,resBottleNeck3,resBottleNeck4,resBottleNeck5,resBottleNeck6,resBottleNeck7,resBottleNeck8};