import os
import json
import trace

basepath = os.getcwd()

logpath = "{}/log".format(basepath)

acc = []
folder = []
for i in range(1,280):
    datapath = "{}/{}/performance.json".format(logpath,i)
    try:
        with open(datapath, 'r') as f:
            scalar = json.load(f)
            acc.append(scalar["acc"])
            folder.append(i)
    except Exception as e:
        trace.Trace()

with open("acc.json" ,"w") as f:
    json.dump(acc, f)

with open("folderlist.json" ,"w") as f:
    json.dump(folder, f)