import snap
from datetime import datetime
import matplotlib.pyplot as plt
import util
import numpy as np
from scipy.stats.stats import pearsonr

edgeFile = 'brightkite/loc-brightkite_edges.txt'
checkinFile = 'brightkite/loc-brightkite_totalCheckins.txt'

# Build the Graphs
userGraph, geoGraph, visitGraph, coordinates, checkins = util.buildGraphs(edgeFile, checkinFile)
userList = []
for node in userGraph.Nodes():
    Id = node.GetId()
    if visitGraph.IsNode(Id):
        userList.append(Id)
locList = []
for node in geoGraph.Nodes():
    Id = node.GetId()
    locNI = visitGraph.GetNI(Id)
    deg = locNI.GetDeg()
    if deg != 0:
        locList.append(Id)

EiFiles = ['degreeIndex_part.txt', 'newRateIndex_part.txt', 'dominanceI2.txt']
BiFiles = ['loc_degreeI.txt', 'loc_edgenumI.txt', 'loc_entropyI.txt']
userMeanCorr = np.zeros((3, 3))
userMeanPvalue = np.zeros((3, 3))
userMedianCorr = np.zeros((3, 3))
userMedianPvalue = np.zeros((3, 3))
locMeanCorr = np.zeros((3, 3))
locMeanPvalue = np.zeros((3, 3))
locMedianCorr = np.zeros((3, 3))
locMedianPvalue = np.zeros((3, 3))
for i in xrange(3):
    for j in xrange(3):
        EiFile = EiFiles[i]
        BiFile = BiFiles[j]
        EiList = []
        with open(EiFile) as f:
            for line in f: EiList.append(float(line.split()[0]))
        Eis = {userList[i]:EiList[i] for i in xrange(len(userList))}
        BiList = []
        with open(BiFile) as f:
            for line in f: BiList.append(float(line.split()[0]))
        Bis = {locList[i]:BiList[i] for i in xrange(len(locList))}
        userMeanBi = []
        userMedianBi = []
        for userId in userList:
            NI = visitGraph.GetNI(userId)
            deg = NI.GetDeg()
            BiList = []
            for k in xrange(deg):
                BiList.append(Bis[NI.GetNbrNId(k)])
            userMeanBi.append(np.average(BiList))
            userMedianBi.append(np.median(BiList))
        c, p = pearsonr(EiList, userMeanBi)
        userMeanCorr[i][j] = c
        userMeanPvalue[i][j] = p
        c, p = pearsonr(EiList, userMedianBi)
        userMedianCorr[i][j] = c
        userMedianPvalue[i][j] = p

        locMeanEi = []
        locMedianEi = []
        for locId in locList:
            NI = visitGraph.GetNI(locId)
            deg = NI.GetDeg()
            EiList = []
            for k in xrange(deg):
                EiList.append(Eis[NI.GetNbrNId(k)])
            locMeanEi.append(np.average(EiList))
            locMedianEi.append(np.median(EiList))
        c, p = pearsonr(BiList, locMeanEi)
        locMeanCorr[i][j] = c
        locMeanPvalue[i][j] = p
        c, p = pearsonr(BiList, locMedianEi)
        locMedianCorr[i][j] = c
        locMedianPvalue[i][j] = p
