import snap
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import random
import numpy as np

edgeFile = 'brightkite/loc-brightkite_edges.txt'
checkinFile = 'brightkite/loc-brightkite_totalCheckins.txt'

# Build the Graphs
userGraph, geoGraph, visitGraph, coordinates, checkins = util.buildGraphs(edgeFile, checkinFile)

# Indexes for locations
degreeI = []
edgeNumI = []
entropyI = []
for node in geoGraph.Nodes():
    locId = node.GetId()
    locNI = visitGraph.GetNI(locId)
    deg = locNI.GetDeg()
    if deg != 0:
        NIdV = snap.TIntV()
        visits = []
        for i in xrange(deg):
            userId = locNI.GetNbrNId(i)
            NIdV.Add(userId)
            EI = visitGraph.GetEI(userId, locId)
            visits.append(visitGraph.GetIntAttrDatE(EI, 'w'))
        subUserGraph = snap.GetSubGraph(userGraph, NIdV)
        numNodes = subUserGraph.GetNodes()
        numEdges = subUserGraph.GetEdges()
        sumDeg = 0
        for node in subUserGraph.Nodes():
            sumDeg += node.GetDeg()
        degreeI.append(1.0 * numNodes / (sumDeg + 0.1))
        edgeNumI.append(1.0 * numEdges / (numNodes ** 2 / 2.0))
        probVisits = [1.0 * visit / sum(visits) for visit in visits]
        entropyI.append(-np.dot(np.array(probVisits), np.log(probVisits)))

with open('loc_degreeI.txt', 'w') as f:
    f.write('\n'.join([str(i) for i in degreeI]))
with open('loc_edgenumI.txt', 'w') as f:
    f.write('\n'.join([str(i) for i in edgeNumI]))
with open('loc_entropyI.txt', 'w') as f:
    f.write('\n'.join([str(i) for i in entropyI]))

n = len(degreeI)
ind = random.sample(range(n), 700000)
a = [degreeI[i] for i in ind]
b = [edgeNumI[i] for i in ind]
c = [entropyI[i] for i in ind]
df = pd.DataFrame({'1/Degree Index':a, 'Edge Number Index': b, 'Entropy Index': c})
pd.tools.plotting.scatter_matrix(df, figsize=(20, 20), diagonal='kde')
plt.savefig('loc_scatter_matrix.png')
plt.close()
