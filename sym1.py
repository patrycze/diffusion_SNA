from igraph import *
import random
import matplotlib.pyplot as plt
import numpy as np
#load data into a graph

def simulation(pp, percentage):

    s = 1;
    isInfecting = True

    g = Graph.Read_Ncol('./net6/1_2.txt', directed=False)

    nodes  = Graph.vcount(g)
    g.vs["label"] = g.vs["name"]
    numberofseeds = int(round(nodes * percentage, ndigits=0))

    infections = 0

    for i in range(0,nodes):
        g.vs[i]["infected"] = 0
        g.vs[i]["used"] = 0

    x = int(random.uniform(nodes, numberofseeds))


    for seeds in range(0, numberofseeds):
        g.vs[g.neighbors(x)[seeds]]["infected"] = 1
        g.vs[g.neighbors(x)[seeds]]["stepinfected"] = 0
        g.vs[g.neighbors(x)[seeds]]["used"] = 0
        g.vs[g.neighbors(x)[seeds]]["color"] = "green"

    while(isInfecting):
        #print("STEP", s)
        infecting = infections
        nodes = Graph.vcount(g)
        for j in range(0,nodes):

            if (g.vs[j]["infected"] == 1 and g.vs[j]["used"] == 0 and g.vs[j]["stepinfected"] != s):
                #print(j)
                g.vs[j]["used"] = 1
                neighborstab = g.neighbors(j, mode=ALL)

                if (len(neighborstab) > 0):
                    n = 0
                    notinfected = []
                    for i in range (0,len(neighborstab)):
                            if(g.vs[neighborstab[i]]["infected"] == 0):
                                notinfected.append(neighborstab[i])
                    #print(notinfected)
                    numberofneighbors = len(notinfected)

                    if notinfected:
                        for k in range(0,numberofneighbors):
                            if(numberofneighbors >= 1):
                                x = random.random()
                                if(x <= pp):
                                    g.vs[notinfected[k]]["infected"] = 1
                                    g.vs[notinfected[k]]["stepinfected"] = s
                                    g.vs[notinfected[k]]["used"] = 0
                                    g.vs[notinfected[k]]["color"] = "blue"

                                    infections = infections + 1

        if(infecting == infections):
            isInfecting = False

        s = s + 1

    #plot(g)
    #print("Zainfekowanych", infections)
    #print("Total coverage % (infections + seeds):")
    #print(100*(numberofseeds + infections)/nodes)
    return infections, s - 1

resultArray = []



spARR = [0.01,0.02,0.03,0.04,0.05]
ppARR = [0.01, 0.05, 0.1, 0.15, 0.20, 0.25]
thefile = open('test.txt', 'w')

for sp in spARR:
    for pp in ppARR:
        for i in range(1,2):
            temp = simulation(pp, sp)
            resultArray.append({
                'sp': sp,
                'pp': pp,
                'infections': temp[0],
                'step': temp[1],
                'run': i
            })

for item in resultArray:
  thefile.write("%s\n" % item)
#print(np.mean(resultArray[0]))