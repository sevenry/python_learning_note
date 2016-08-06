
from numpy import *

def loadDataSet(fileName):      
    dataMat = []              
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = list(map(float,curLine))###map()返回值已经不再是list,而是iterators；所以需要将iterator 转换成list，即list(map()) 
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA, vecB):##欧几里得距离
    return sqrt(sum(power(vecA - vecB, 2))) 

def randCent(dataSet, k):##生成k个中心
    n = shape(dataSet)[1]##列数
    centroids = mat(zeros((k,n)))
    for j in range(n):
        minJ = min(dataSet[:,j])#每一列最值 
        #print(minJ)
        rangeJ = float(max(dataSet[:,j]) - minJ)#最大值与最小值差
        #print(rangeJ)
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))#生成k*1的矩阵，每个数在最小值和最大值之间。
    return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):##得到k近邻中心和每个数据最近的中心分布。
    m = shape(dataSet)[0]#行数
    #print(m)
    clusterAssment = mat(zeros((m,2)))
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf; minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])#测量每个数据与每个中心的距离
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex: clusterChanged = True##只要原数据中有一个点对应的最近的距离点编号有改变就再次循环。
            ##如果所有的数据对应的最近的中心点不发生任何改变，则在下一个循环中每一个中心点所收集的原数据相同，则不会生成新的k近邻点。
            ##所有最后一次调用时下面的部分多余。可以考虑添加if判断停止循环。
            clusterAssment[i,:] = minIndex,minDist**2##存储最近的中心点及距离平方
        #print (centroids)
        if clusterChanged==False:return centroids, clusterAssment##最后一次循环可省略下面的for循环部分。
        for cent in range(k):#recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#最后的[0]是输出的符合要求的点的存储点号的原数据
            ##这里nonzero内部的值是True,False；返回的是True值的位置。
            #比如aaa=mat([[0,1],[1,1]]),nonzero(aaa[:,0].A==0)，aaa[:,0].A==0 返回的是 True, False; 所以nonzero返回的是array[0]，array[0]
            #print(ptsInClust)
            #print(shape(ptsInClust))
            centroids[cent,:] = mean(ptsInClust, axis=0) #
        #print(centroids)
        #print()
    return centroids, clusterAssment

def biKmeans(dataSet, k, distMeas=distEclud):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    #print(centroid0)#
    centList =[centroid0]
    #print(len(centList))#1
    for j in range(m):#calc initial Error
        clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2 #第二项存储中心点与每个数据距离平方
    while (len(centList) < k):#k限制了总的循环次数
        lowestSSE = inf
        for i in range(len(centList)):
            #print(i)
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]
            #aido=dataSet[nonzero(clusterAssment[:,0].A==i)[0]]#和上面的写法结果一致。
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)#对剥离出来的部分数据采取k近邻方法，生成2个近邻点。
            #print(shape(splitClustAss))
            sseSplit = sum(splitClustAss[:,1])##
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])#第一次循环到这里时所有都为0，即该行为空。因为初始设定时值没有改变。
            #第二次循环到这里时，假设此时i=0，则计算前次分组i=1时的所有距离。而sseSplit计算的是前次分组i=0时的数据中再次划分两个点之后的所有距离。
            #print(shape(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1]))
            #print ("sseSplit, and notSplit: ",sseSplit,sseNotSplit)
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        print(lowestSSE)
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList) 
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
        #print(len(centList))
        #print(shape(bestClustAss))
        #print ('the bestCentToSplit is: ',bestCentToSplit)
        #print ('the len of bestClustAss is: ', len(bestClustAss))
        centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]#replace a centroid with two best centroids 
        centList.append(bestNewCents[1,:].tolist()[0])##这两行需要先转成list才能最后运行mat()
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss
    return mat(centList), clusterAssment

import urllib.request
import json
def geoGrab(stAddress, city):
    apiStem = 'http://where.yahooapis.com/geocode?'  #create a dict and constants for the goecoder
    params = {}
    params['flags'] = 'J'#JSON return type
    params['appid'] = 'ppp68N8t'
    params['location'] = '%s %s' % (stAddress, city)
    url_params = urllib.parse.urlencode(params)
    yahooApi = apiStem + url_params      #print url_params
    print (yahooApi)
    c=urllib.request.urlopen(yahooApi)
    return json.loads(c.read())

from time import sleep
def massPlaceFind(fileName):
    fw = open('places.txt', 'w')
    for line in open(fileName).readlines():
        line = line.strip()
        lineArr = line.split('\t')
        retDict = geoGrab(lineArr[1], lineArr[2])
        if retDict['ResultSet']['Error'] == 0:
            lat = float(retDict['ResultSet']['Results'][0]['latitude'])
            lng = float(retDict['ResultSet']['Results'][0]['longitude'])
            print ("%s\t%f\t%f" % (lineArr[0], lat, lng))
            fw.write('%s\t%f\t%f\n' % (line, lat, lng))
        else: print ("error fetching")
        sleep(1)
    fw.close()
















