
def readTol(accPath,lossPath):
    acc = None
    loss = None
    tol = [[],[],[]]
    
    with open(accPath,"r") as f:
        acc = f.readlines()
    with open(lossPath,"r") as f:
        loss = f.readlines()
    for i in acc:
        d = i.strip().split(",")
        tol[0].append(d[0])
        tol[2].append(d[1])
    for i in loss:
        d = i.strip().split(",")
        tol[1].append(d[0])
    return tol
def readBreakpoints(dPath):
    paths = dPath.split("/")
    paths.pop()
    paths.pop()
    breakpoints = []
    rpath = paths[0]
    paths.pop(0)
    for i in paths:
        rpath = "{}/{}".format(rpath,i)
        if i == "model_0" or "model" not in i:
            continue
        else:
            
            with open("{}/0/re.text".format(rpath),"r") as f:
                breakpoints.append(int(f.readline().strip()))
    return breakpoints

def correctBreakpoints(step,breakpoints):
    for i in range(len(breakpoints)):
        for j in range(len(step)):
            if int(step[j]) >= breakpoints[i]:
                breakpoints[i] = j-1
                break

def scalar_read(job, index = 0):
    path = "Prun/data/{}/control.txt".format(job)
    accPath = "Prun/data/{}/__cache__/myscalar/accuracy.txt".format(job)
    lossPath = "Prun/data/{}/__cache__/myscalar/loss.txt".format(job)

    dPath = None
    with open(path,"r") as f:
        path_ = f.readline().strip()
        segs = path_.split("@")
        dPath = segs[11]
        
    breakpoints = readBreakpoints(dPath)

    tol = readTol(accPath,lossPath)
    correctBreakpoints(tol[2],breakpoints)
    return {"tol":tol,"breakpoints":breakpoints}