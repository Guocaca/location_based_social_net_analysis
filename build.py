import snap
from datetime import datetime
import matplotlib.pyplot as plt
import util
import collections

edgeFile = 'brightkite/loc-brightkite_edges.txt'
checkinFile = 'brightkite/loc-brightkite_totalCheckins.txt'

# Build the Graphs
userGraph, geoGraph, visitGraph, coordinates, checkins = util.buildGraphs(edgeFile, checkinFile)

# Degree distributions
util.userDeg(userGraph)
util.geoDeg(geoGraph)
util.visitDeg(visitGraph)

for graph in [userGraph, geoGraph, visitGraph]:
    print graph.GetNodes()
    print graph.GetEdges()
    print 1.0 * snap.GetMxWcc(graph).GetNodes() / userGraph.GetNodes()
    print 1.0 * snap.GetMxWcc(graph).GetEdges() / userGraph.GetEdges()
    if graph != visitGraph:
        print snap.GetClustCf(graph)
