import snap
from datetime import datetime
import matplotlib.pyplot as plt
import util
import collections
import pandas as pd

edgeFile = 'brightkite/loc-brightkite_edges.txt'
checkinFile = 'brightkite/loc-brightkite_totalCheckins.txt'

# Build the Graphs
userGraph, geoGraph, visitGraph, coordinates, checkins = util.buildGraphs(edgeFile, checkinFile)

# Degree distributions
util.userDeg(userGraph)
util.geoDeg(geoGraph)
util.visitDeg(visitGraph)

# Get indexes for users (users who haven't checked in are considered 0)
userNum = userGraph.GetNodes()
placeNumI = []
newRateI = []
for NId in xrange(userNum):
    if NId in checkins.keys():
        checkinfo = checkins[NId]
        timeline = sorted(checkinfo.items(), key = lambda x:x[0])
        places = [item[1] for item in timeline]
        placeNumI.append(len(set(places)))
        if len(places) == 1:
            newRateI.append(0.0)
        else:
            oldIndex = len(places) / 2
            old = set(places[0:oldIndex])
            newVisit = 0
            for k in places[oldIndex:]:
                if k not in old:
                    newVisit += 1
            newRateI.append(1.0 * newVisit / (len(places) - oldIndex))
    else:
        placeNUmI.append(0.0)
        newRateI.append(0.0)

# Plot newRateI
new = dict(collections.Counter(newRateI))
sortednew = sorted(new.items(), key = lambda x:x[0], reverse = True)
x = [item[0] for item in sortednew]
y = [item[1] for item in sortednew]
plt.plot(x, y, color = '#088da5')
plt.xscale('log')
plt.yscale('log')
plt.xlim(xmax = 1)
plt.xlabel('New Rate Index')
plt.ylabel('Frequency')
plt.savefig('newrate_dist.pdf')
plt.close()

# Calculate dominantIndex for users (the radius is dominant by first k places)
deltas = [0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
labels = ['delta = ' + str(i) for i in deltas]
plots = [None] * 6
for i in xrange(6):
    delta = deltas[i]
    dominant = []
    dominantRate = []
    for node in userGraph.Nodes():
        NId = node.GetId()
        if NId in checkins.keys():
            checkinfo = checkins[NId]
            timeline = sorted(checkinfo.items(), key = lambda x:x[0])
            places = [item[1] for item in timeline]
            R = util.radius(places, coordinates, Pmc)
            for k in xrange(1, placeNum + 1):
                if util.radius(places, coordinates， k) >= delta * R:
                    # dominantRate.append(100.0 * k / placeNum)
                    dominant.append(k)
                    break
    domi = dict(collections.Counter(dominant))
    sorteddomi = sorted(domi.items(), key = lambda x:x[0], reverse = True)
    x = [item[0] for item in sorteddomi]
    y = [item[1] for item in sorteddomi]
    plt.plot(x, y)
    plots[i] ,= plt.plot(x, y)
plt.xscale('log')
plt.yscale('log')
plt.legend(tuple(plots), tuple(labels))
plt.xlabel('Dominance Index')
plt.ylabel('Frequency')
plt.savefig('dominant_dist.pdf')


newRateI = []
with open('newRateIndex_part.txt') as f:
    for line in f: newRateI.append(float(line.split()[0]))
placeNumI = []
with open('degreeIndex_part.txt') as f:
    for line in f: placeNumI.append(int(line.split()[0]))
dominanceI = []
with open('dominanceI2.txt') as f:
    for line in f: dominanceI.append(int(line.split()[0]))

df = pd.DataFrame({'Degree Index':placeNumI, 'New Rate Index': newRateI, 'Dominance Index': dominanceI})
pd.tools.plotting.scatter_matrix(df, alpha=0.2, figsize=(20, 20), diagonal='kde')
plt.savefig('user_scatter_matrix.png')
plt.close()
