import json
def reader(job,op,taskUid,graph):
    path = "Prun/data/{}/graph".format(job)
    with open("{}/{}.json".format(path,taskUid),"r") as f:
        graph = json.load(f)
        
    return graph