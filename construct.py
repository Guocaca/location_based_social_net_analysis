import snap
from datetime import datetime
import matplotlib.pyplot as plt

edgeFile = 'brightkite/loc-brightkite_edges.txt'
checkinFile = 'brightkite/loc-brightkite_totalCheckins.txt'

# Construct the userGraph from edgeFile
userGraph = snap.TUNGraph.New()
with open(edgeFile) as f:
    for line in f:
        a, b = line.split()
        a, b = int(a), int(b)
        if not userGraph.IsNode(a): userGraph.AddNode(a)
        if not userGraph.IsNode(b): userGraph.AddNode(b)
        userGraph.AddEdge(a, b)

# Extrax=ct the information from checkinFile
checkins = {}
coordinates = {}
locNames = set([])
userIds = set([])
with open(checkinFile) as f:
    for i, line in enumerate(f):
        if i % 100000 == 0:
            print i / 100000
        ss = line.split()
        if len(ss) != 5: continue
        user = int(ss[0])
        # time = datetime.strptime(ss[1], '%Y-%m-%dT%H:%M:%SZ')
        time = ss[1]
        loc = ss[-1]
        if loc not in locNames:
            coordinates[loc] = (float(ss[2]), float(ss[3]))
            locNames.add(loc)
        if user not in userIds:
            checkins[user] = {}
            userIds.add(user)
        checkins[user][time] = loc

# Redefine simpler location IDs
locations = list(locNames)
reverseLoc = {locations[i]: -(i + 2) for i in xrange(len(locations))}
for user in checkins.keys():
    for time in checkins[user].keys():
        loc = checkins[user][time]
        checkins[user][time] = reverseLoc[loc]

# Construct geographical graph
geoGraph = snap.TNEANet.New()
geoGraph.AddIntAttrE("w")
for i in xrange(len(locations)):
    geoGraph.AddNode(-(i + 2))
for cIn in checkins.values():
    timeline = sorted(cIn.items(), key = lambda x: x[0])
    for i in xrange(0, len(timeline) - 1):
        a = timeline[i][1]
        b = timeline[i + 1][1]
        if geoGraph.IsEdge(a, b):
            EI = geoGraph.GetEI(a, b)
            geoGraph.AddIntAttrDatE(EI, geoGraph.GetIntAttrDatE(EI, 'w') + 1, 'w')
        elif a != b:
            geoGraph.AddEdge(a, b)
            EI = geoGraph.GetEI(a, b)
            geoGraph.AddIntAttrDatE(EI, 1, 'w')

# Construct visitGraph between the layers of people and places
visitGraph = snap.TNEANet.New()
for user in checkins.keys():
    visitGraph.AddNode(user)
for i in xrange(len(locations)):
    visitGraph.AddNode(-(i + 2))

visitGraph.AddIntAttrE('w')
for user in checkins.keys():
    for time in checkins[user].keys():
        loc = checkins[user][time]
        if visitGraph.IsEdge(user, loc):
            EI = visitGraph.GetEI(user, loc)
            visitGraph.AddIntAttrDatE(EI, visitGraph.GetIntAttrDatE(EI, 'w') + 1, 'w')
        else:
            visitGraph.AddEdge(user, loc)
            EI = visitGraph.GetEI(user, loc)
            visitGraph.AddIntAttrDatE(EI, 1, 'w')

# Degree distribution of userGraph
userNum = userGraph.GetNodes()
degrees = list()
counts = list()
DegToCntV = snap.TIntPrV()
snap.GetDegCnt(userGraph, DegToCntV)
for item in DegToCntV:
    degrees.append(item.GetVal1())
    counts.append(item.GetVal2())
# Normalize the counts
counts = [value / (1.0 * userNum) for value in counts]

plt.plot(degrees, counts, color = "#fa8072")
plt.xscale('log')
plt.yscale('log')
plt.title('Degree Distribution for User-User Network')
plt.xlabel('degree')
plt.ylabel('frequency')
plt.savefig('degree-user-user.pdf')
plt.close()

# Degree distribution of geoGraph
locNum = geoGraph.GetNodes()
degreesLoc = list()
countsLoc = list()
DegToCntV = snap.TIntPrV()
snap.GetDegCnt(geoGraph, DegToCntV)
for item in DegToCntV:
    degreesLoc.append(item.GetVal1())
    countsLoc.append(item.GetVal2())
# Normalize the counts
counts = [value / (1.0 * locNum) for value in counts]

plt.plot(degreesLoc, countsLoc, color = "#fa8072")
plt.xscale('log')
plt.yscale('log')
plt.title('Degree Distribution for Place-Place Network')
plt.xlabel('degree')
plt.ylabel('frequency')
plt.savefig('degree-loc-loc.pdf')
plt.close()

# Degree distribution of visitGraph
degreeUser = {}
degreeLoc = {}
for node in visitGraph.Nodes():
    NId = node.GetId()
    d = node.GetDeg()
    if NId >= 0:
        print NId
        if d in degreeUser.keys(): degreeUser[d] += 1
        else: degreeUser[d] = 1
    else:
        if d in degreeLoc.keys(): degreeLoc[d] += 1
        else: degreeLoc[d] = 1

dU = sorted(degreeUser.items(), key = lambda x: x[0])
dL = sorted(degreeLoc.items(), key = lambda x: x[0])
degreesUser = [item[0] for item in dU]
countsUser = [item[1] for item in dU]
degreesLoc = [item[0] for item in dL]
countsLoc = [item[1] for item in dL]

# Normalize the counts
numUser = sum(countsUser)
numLoc = sum(countsLoc)
countsUser = [value / (1.0 * numUser) for value in countsUser]
countsLoc = [value / (1.0 * numLoc) for value in countsLoc]

plt.plot(degreesUser, countsUser, color = "#fa8072")
plt.xscale('log')
plt.yscale('log')
plt.title("User's Degree Distribution for User-Place Network")
plt.xlabel('degree')
plt.ylabel('frequency')
plt.savefig('degree-user-loc.pdf')
plt.close()

plt.plot(degreesLoc, countsLoc, color = "#fa8072")
plt.xscale('log')
plt.yscale('log')
plt.title("Place's Degree Distribution for User-Place Network")
plt.xlabel('degree')
plt.ylabel('frequency')
plt.savefig('degree-loc-user.pdf')
plt.close()
