import json
def saver(job,op,taskUid,graph):
    path = "Prun/data/{}/graph".format(job)
    with open("{}/{}.json".format(path,taskUid),"w") as f:
        json.dump(graph,f)
    
    return "success"