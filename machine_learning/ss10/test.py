import kMeans
from numpy import *



datMat=mat(kMeans.loadDataSet('testSet.txt'))
#print(shape(datMat[:,0]))
'''
print(min(datMat[:,0]))
print(min(datMat[:,1]))

print(max(datMat[:,0]))
print(max(datMat[:,1]))
'''
#print(kMeans.randCent(datMat,2))
#print(kMeans.distEclud(datMat[0],datMat[1]))

#myCentroids, clustAssing= kMeans.kMeans(datMat,4)

datMat3=mat(kMeans.loadDataSet('testSet2.txt'))
#centList,myNewAssments=kMeans.biKmeans(datMat3,9)

#print(centList)

geoResults=kMeans.geoGrab('1 VA Center', 'Augusta, ME')
