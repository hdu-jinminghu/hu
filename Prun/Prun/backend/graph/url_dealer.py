import json
from .graph_reader import reader
from .graph_saver import saver
def graphUrlDealer(request):
    postBody  = request.body
    postBody = json.loads(postBody)
    job = postBody["job"]
    op = postBody["op"]
    taskUid = postBody["uid"]
    graph = postBody["graph"]
    res = None
    if op == "save":
        res = saver(job,op,taskUid,graph)
    elif op == "read":
        res = reader(job,op,taskUid,graph)
    
    return res